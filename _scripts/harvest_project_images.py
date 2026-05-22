import os
import sys
import re
import csv
import time
import requests
from urllib.parse import urlparse
from io import BytesIO
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import imagehash

# Ensure we can import neo4j_env from the same directory
current_dir = Path(__file__).parent.resolve()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    import neo4j_env
    from neo4j import GraphDatabase
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    sys.exit(1)

# Config
BASE_DIR = Path(r"E:\recherche\_images")
METADATA_CSV = BASE_DIR / "project_images_metadata.csv"
MIN_IMAGES = 3
MAX_IMAGES = 7
HASH_THRESHOLD = 5 

HEADERS = {
    'User-Agent': 'RechercheImageHarvester/4.0 (https://github.com/example; bot@example.org) requests/2.31.0'
}

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name.replace('/', '_'))

def get_projects_context_from_neo4j():
    uri, user, pwd, db = neo4j_env.resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    
    query = """
    MATCH (p)
    WHERE (p:Projekt OR p:Programm) AND p.name IS NOT NULL
    OPTIONAL MATCH (p)-[:LIEGT_IN_STADT]->(s:Stadt)
    OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
    OPTIONAL MATCH (a:Akteur)-[:BETEILIGT_AN]->(p)
    RETURN p.id AS id, p.name AS name, s.name AS city, l.name AS country, collect(DISTINCT a.name) AS actors
    """
    projects = []
    try:
        result = driver.execute_query(query, database_=db)
        for record in result.records:
            projects.append({
                "id": record["id"],
                "name": record["name"],
                "city": record["city"],
                "country": record["country"],
                "actors": record["actors"]
            })
    finally:
        driver.close()
    return projects

def search_wikimedia(query):
    time.sleep(1)
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "format": "json",
        "gsrlimit": 15
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        results = []
        for page_id, page_data in pages.items():
            title = page_data.get("title", "")
            imageinfo = page_data.get("imageinfo", [{}])[0]
            img_url = imageinfo.get("url")
            if img_url:
                extmetadata = imageinfo.get("extmetadata", {})
                author = re.sub(r'<[^>]+>', '', extmetadata.get("Artist", {}).get("value", ""))
                desc = re.sub(r'<[^>]+>', '', extmetadata.get("ImageDescription", {}).get("value", ""))
                license_info = extmetadata.get("LicenseShortName", {}).get("value", "")
                categories = extmetadata.get("Categories", {}).get("value", "")
                
                results.append({
                    "url": img_url,
                    "title": title,
                    "description": desc,
                    "author": author,
                    "categories": categories,
                    "license": license_info,
                    "source": "Wikimedia"
                })
        return results
    except Exception as e:
        print(f"Wikimedia API error for '{query}': {e}")
        return []

def search_openverse(query):
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": query,
        "page_size": 15
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 429:
            time.sleep(2)
        if response.status_code != 200:
            return []
        data = response.json()
        results = []
        for item in data.get("results", []):
            tags = " ".join([t.get("name", "") for t in item.get("tags", [])])
            results.append({
                "url": item.get("url"),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "author": item.get("creator", ""),
                "categories": tags,
                "license": item.get("license", ""),
                "source": "Openverse"
            })
        return results
    except Exception as e:
        print(f"Openverse API error for '{query}': {e}")
        return []

def download_and_hash_image(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        if image.mode != "RGB":
            image = image.convert("RGB")
        h = imagehash.phash(image)
        return image, response.content, h
    except Exception as e:
        return None, None, None

def is_unique(new_hash, existing_hashes):
    for h in existing_hashes:
        if new_hash - h <= HASH_THRESHOLD:
            return False
    return True

def evaluate_image(image_data, project):
    score = 0
    text_to_search = f"{image_data['title']} {image_data['description']} {image_data['author']} {image_data.get('categories', '')}".lower()
    cats_and_tags = image_data.get('categories', '').lower()
    
    # 1. Reject blatantly wrong subjects immediately based on tags/categories
    non_arch_keywords = ['portrait', 'person', 'car', 'vehicle', 'auto', 'man', 'woman', 'people', 'coin', 'stamp', 'seal', 'insect', 'animal', 'hybrid', 'sculptuur', 'sculpture', 'painting', 'drawing']
    if any(kw in cats_and_tags for kw in non_arch_keywords) or any(f" {kw} " in text_to_search for kw in non_arch_keywords):
        return 0 # Instant fail
        
    # 2. Check for Explicit Architecture / Building tags
    arch_keywords = ['architecture', 'building', 'pavilion', 'facade', 'structure', 'architektur', 'bauwerk', 'hq', 'headquarters', 'office', 'kantoor', 'gebouw', 'huis', 'house', 'construction', 'halle', 'werkhof', 'campus', 'exterior']
    has_arch = any(kw in cats_and_tags for kw in arch_keywords) or any(kw in text_to_search for kw in arch_keywords)
    
    reuse_keywords = ['reuse', 'reclaimed', 'circular', 'wiederverwendung', 'recycled', 'spolia', 'bauteil', 'salvage', 'upcycling', 'zirkulär']
    has_reuse = any(kw in cats_and_tags for kw in reuse_keywords) or any(kw in text_to_search for kw in reuse_keywords)

    # 3. Base Name check
    raw_name_clean = re.sub(r'\(.*?\)', '', project["name"].lower())
    
    # Exact Phrase Match
    phrases = [p.strip() for p in re.split(r'[,/]', raw_name_clean) if len(p.strip()) > 4]
    exact_phrase_match = any(p in text_to_search for p in phrases)
    if exact_phrase_match:
        score += 60
        
    # Word Match
    name_words = [w for w in raw_name_clean.replace('/', ' ').replace(',', ' ').replace('-', ' ').split() if len(w) > 3]
    matched_words = sum(1 for w in name_words if w in text_to_search)
    if len(name_words) > 0:
        score += (matched_words / len(name_words)) * 40 
        
    # 4. Context Context checks
    has_city = False
    if project["city"] and project["city"].lower() in text_to_search:
        has_city = True
        score += 30
        
    has_actor = False
    for actor in project["actors"]:
        if actor and len(actor)>3 and actor.lower() in text_to_search:
            has_actor = True
            score += 35
            
    if has_arch: score += 25
    if has_reuse: score += 35
    
    # The image must match AT LEAST ONE architectural keyword to guarantee it's not random.
    if not has_arch and not has_reuse:
        # If it doesn't say building, architecture, reuse, etc... we reject it, UNLESS it's an incredibly specific name match + city + actor
        if not (exact_phrase_match and has_city and has_actor):
            return 0
            
    # We must have at least SOME relation to the project name, or the city+architect combo
    if matched_words == 0 and not (has_city and has_actor):
        return 0

    return score

def get_base_name(raw_name):
    clean_name = re.sub(r'\(.*?\)', '', raw_name)
    parts = re.split(r'[,/]', clean_name)
    parts = [p.strip() for p in parts if len(p.strip()) > 3]
    if parts:
        return parts[0]
    return raw_name.strip()

def harvest_images():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    metadata_exists = METADATA_CSV.exists()
    
    projects = get_projects_context_from_neo4j()
    print(f"Found {len(projects)} projects. Using V4 STRICT CATEGORY EVALUATOR.")
    
    with open(METADATA_CSV, mode="a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["project_id", "project_name", "eval_score", "source_api", "source_title", "source_url", "local_path", "license", "author", "image_hash"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not metadata_exists:
            writer.writeheader()
        
        for project in projects:
            proj_id = project["id"]
            proj_name = project["name"]
            safe_name = sanitize_filename(proj_name)
            proj_dir = BASE_DIR / safe_name
            
            if proj_dir.exists():
                existing_files = list(proj_dir.glob("*.*"))
                if len(existing_files) >= MAX_IMAGES:
                    continue
            
            proj_dir.mkdir(parents=True, exist_ok=True)
            print(f"Processing '{proj_name}'...")
            
            base_name = get_base_name(proj_name)
            
            queries = [
                f'"{base_name}" architecture',
                f'{base_name} building',
                f'{base_name} reuse',
                f'{base_name} wiederverwendung'
            ]
            if project["city"]:
                queries.append(f'{base_name} {project["city"]}')
            if project["actors"]:
                queries.append(f'{base_name} {project["actors"][0]}')
                
            queries = list(dict.fromkeys(queries))
                
            collected_images = 0
            existing_hashes = []
            
            for query in queries:
                if collected_images >= MAX_IMAGES:
                    break
                
                print(f"  Searching: '{query}'...")
                candidates = []
                candidates.extend(search_wikimedia(query))
                candidates.extend(search_openverse(query))
                
                for cand in candidates:
                    if collected_images >= MAX_IMAGES:
                        break
                    
                    url = cand["url"]
                    if not url: continue
                    
                    parsed_url = urlparse(url)
                    ext_check = Path(parsed_url.path).suffix.lower().lstrip('.')
                    if ext_check in ['pdf', 'djvu', 'ogg', 'webm', 'mp4', 'svg', 'doc', 'docx', 'zip', 'gz', 'txt']:
                        continue
                    
                    # ---- CATEGORY + SMART EVALUATION ----
                    score = evaluate_image(cand, project)
                    if score < 60:
                        continue 
                        
                    img, raw_data, h = download_and_hash_image(url)
                    if not h: continue
                    
                    if is_unique(h, existing_hashes):
                        existing_hashes.append(h)
                        ext = url.split('.')[-1].split('?')[0].lower()
                        if ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                            ext = 'jpg'
                        
                        filename = f"{proj_id}_{collected_images+1}_{h}.{ext}"
                        filepath = proj_dir / filename
                        
                        with open(filepath, "wb") as f:
                            f.write(raw_data)
                            
                        writer.writerow({
                            "project_id": proj_id,
                            "project_name": proj_name,
                            "eval_score": score,
                            "source_api": cand["source"],
                            "source_title": cand["title"].encode('ascii', 'ignore').decode('utf-8'),
                            "source_url": url,
                            "local_path": str(filepath),
                            "license": cand["license"],
                            "author": cand["author"].encode('ascii', 'ignore').decode('utf-8'),
                            "image_hash": str(h)
                        })
                        csvfile.flush()
                        
                        collected_images += 1
                        print(f"    [Score: {score}] VERIFIED ARCHITECTURE! Saved image {collected_images}/{MAX_IMAGES}")
                        
            print(f"  Finished '{proj_name}'. Valid architectural images saved: {collected_images}")

if __name__ == "__main__":
    harvest_images()
