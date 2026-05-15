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
    'User-Agent': 'RechercheImageHarvester/3.0 (https://github.com/example; bot@example.org) requests/2.31.0'
}

REUSE_KEYWORDS = ['reuse', 'reclaimed', 'circular', 'wiederverwendung', 'recycled', 'spolia', 'bauteil', 'salvage', 'upcycling', 'zirkulär']

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name.replace('/', '_'))

def get_projects_context_from_neo4j():
    uri, user, pwd, db = neo4j_env.resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    
    query = """
    MATCH (p:Projekt)
    WHERE p.name IS NOT NULL
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
        response.raise_for_status()
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
                
                results.append({
                    "url": img_url,
                    "title": title,
                    "description": desc,
                    "author": author,
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
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "url": item.get("url"),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "author": item.get("creator", ""),
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
    text_to_search = f"{image_data['title']} {image_data['description']} {image_data['author']}".lower()
    
    # 1. Base Name check
    raw_name = project["name"].lower()
    clean_name = re.sub(r'\(.*?\)', '', raw_name).split(',')[0].split('/')[0].strip()
    
    name_words = [w for w in clean_name.split() if len(w) > 3]
    word_matches = sum(1 for w in name_words if w in text_to_search)
    
    if clean_name and len(clean_name) > 4 and clean_name in text_to_search:
        score += 60 # Exact name match is almost a guaranteed pass
    elif len(name_words) > 0 and word_matches == len(name_words):
        score += 50 # All long words found (even if split apart)
    elif word_matches > 0:
        score += 20 * word_matches # Partial name match
        
    # 2. Context checks
    if project["city"] and project["city"].lower() in text_to_search:
        score += 25
        
    for actor in project["actors"]:
        if actor and len(actor)>3 and actor.lower() in text_to_search:
            score += 35
            
    # 3. Reuse / Architecture keyword checks
    if any(kw in text_to_search for kw in REUSE_KEYWORDS):
        score += 30
    if any(kw in text_to_search for kw in ['architecture', 'building', 'pavilion', 'facade', 'structure', 'architektur', 'bauwerk']):
        score += 15

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
    print(f"Found {len(projects)} projects. Using SMART REUSE EVALUATOR.")
    
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
            
            # Broaden queries but rely on the smart evaluator to save us
            queries = [
                f'"{base_name}"', # Exact phrase
                f'{base_name} architecture', # Broad words
                f'{base_name} reuse',
                f'{base_name} wiederverwendung'
            ]
            if project["city"]:
                queries.append(f'{base_name} {project["city"]}')
            if project["actors"]:
                queries.append(f'{project["actors"][0]} architecture')
                
            # Remove duplicate queries
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
                    
                    # ---- SMART EVALUATION ----
                    # Target score: 55
                    # Needs either: Exact Name (60) OR (All words(50) + Architecture(15)) OR (Actor(35) + Partial(20)) OR (Partial(20) + Reuse(30) + Building(15))
                    score = evaluate_image(cand, project)
                    if score < 55:
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
                        print(f"    [Score: {score}] MATCH! Saved image {collected_images}/{MAX_IMAGES}")
                        
            print(f"  Finished '{proj_name}'. Valid architectural/reuse images saved: {collected_images}")

if __name__ == "__main__":
    harvest_images()
