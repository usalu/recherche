import os
import sys
import re
import time
import requests
from urllib.parse import urlparse, quote
from pathlib import Path

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
HEADERS = {
    'User-Agent': 'RechercheImageReviewAssistant/1.0 (bot@example.org) requests/2.31.0'
}
SCORE_THRESHOLD = 50  # Lower threshold since it's just for review, user can reject

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
    OPTIONAL MATCH (p)-[:HAT_NUTZUNG]->(n:Nutzung)
    RETURN p.id AS id, p.name AS name, s.name AS city, l.name AS country, 
           collect(DISTINCT a.name) AS actors, collect(DISTINCT n.name) AS typologies
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
                "actors": record["actors"],
                "typologies": record["typologies"]
            })
    finally:
        driver.close()
    return projects

def search_wikimedia(query):
    time.sleep(0.5)
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "format": "json",
        "gsrlimit": 10
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code != 200: return []
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
                    "thumb_url": imageinfo.get("thumburl", img_url),
                    "title": title,
                    "description": desc,
                    "author": author,
                    "categories": categories,
                    "license": license_info,
                    "source": "Wikimedia Commons",
                    "source_link": imageinfo.get("descriptionurl", img_url)
                })
        return results
    except Exception as e:
        return []

def search_openverse(query):
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": query,
        "page_size": 10
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 429:
            time.sleep(1)
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code != 200: return []
        data = response.json()
        results = []
        for item in data.get("results", []):
            tags = " ".join([t.get("name", "") for t in item.get("tags", [])])
            results.append({
                "url": item.get("url"),
                "thumb_url": item.get("thumbnail", item.get("url")),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "author": item.get("creator", ""),
                "categories": tags,
                "license": item.get("license", ""),
                "source": "Openverse",
                "source_link": item.get("foreign_landing_url", item.get("url"))
            })
        return results
    except Exception as e:
        return []

def search_wikidata(query):
    time.sleep(0.5)
    search_url = "https://www.wikidata.org/w/api.php"
    search_params = {
        "action": "wbsearchentities",
        "search": query,
        "language": "en",
        "format": "json",
        "limit": 3
    }
    try:
        res = requests.get(search_url, params=search_params, headers=HEADERS, timeout=10)
        if res.status_code != 200: return []
        entities = res.json().get("search", [])
        
        results = []
        for entity in entities:
            entity_id = entity.get("id")
            if not entity_id: continue
            
            # Get claims for this entity
            claims_url = f"https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={entity_id}&property=P18&format=json"
            claims_res = requests.get(claims_url, headers=HEADERS, timeout=10)
            if claims_res.status_code != 200: continue
            
            claims_data = claims_res.json().get("claims", {})
            p18 = claims_data.get("P18", [])
            for claim in p18:
                filename = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
                if filename:
                    # Query Wikimedia Commons for the file URL
                    file_query = f"File:{filename}"
                    wm_results = search_wikimedia(file_query)
                    for wm_res in wm_results:
                        wm_res["source"] = f"Wikidata Entity: {entity.get('label', entity_id)}"
                        results.append(wm_res)
        return results
    except Exception as e:
        return []

def evaluate_image(image_data, project):
    score = 0
    reasons = []
    
    text_to_search = f"{image_data['title']} {image_data['description']} {image_data['author']} {image_data.get('categories', '')}".lower()
    cats_and_tags = image_data.get('categories', '').lower()
    
    # 1. Reject blatantly wrong subjects
    non_arch_keywords = ['portrait', 'person', 'car', 'vehicle', 'auto', 'man', 'woman', 'people', 'coin', 'stamp', 'seal', 'insect', 'animal', 'hybrid', 'painting', 'drawing']
    if any(kw in cats_and_tags for kw in non_arch_keywords):
        return 0, ["Rejected: Matched non-architectural tag"]
        
    # 2. Keywords
    arch_keywords = ['architecture', 'building', 'pavilion', 'facade', 'structure', 'architektur', 'bauwerk', 'hq', 'headquarters', 'office', 'kantoor', 'gebouw', 'huis', 'house', 'construction', 'halle', 'werkhof', 'campus', 'exterior']
    has_arch = any(kw in cats_and_tags for kw in arch_keywords) or any(kw in text_to_search for kw in arch_keywords)
    
    reuse_keywords = ['reuse', 'reclaimed', 'circular', 'wiederverwendung', 'recycled', 'spolia', 'bauteil', 'salvage', 'upcycling', 'zirkulär']
    has_reuse = any(kw in cats_and_tags for kw in reuse_keywords) or any(kw in text_to_search for kw in reuse_keywords)

    # 3. Base Name check
    raw_name_clean = re.sub(r'\(.*?\)', '', project["name"].lower())
    phrases = [p.strip() for p in re.split(r'[,/]', raw_name_clean) if len(p.strip()) > 4]
    
    exact_phrase_match = any(p in text_to_search for p in phrases)
    if exact_phrase_match:
        score += 60
        reasons.append("Exact Project Name Match")
        
    name_words = [w for w in raw_name_clean.replace('/', ' ').replace(',', ' ').replace('-', ' ').split() if len(w) > 3]
    matched_words = sum(1 for w in name_words if w in text_to_search)
    if len(name_words) > 0 and matched_words > 0:
        ratio = matched_words / len(name_words)
        score += ratio * 40
        if not exact_phrase_match:
            reasons.append(f"Partial Name Match ({int(ratio*100)}%)")
        
    # 4. Context checks
    has_city = False
    if project["city"] and project["city"].lower() in text_to_search:
        has_city = True
        score += 30
        reasons.append("City Match")
        
    has_actor = False
    for actor in project["actors"]:
        if actor and len(actor)>3 and actor.lower() in text_to_search:
            has_actor = True
            score += 35
            reasons.append(f"Actor Match ({actor})")
            
    if has_arch:
        score += 25
        reasons.append("Architecture Keyword")
    if has_reuse:
        score += 35
        reasons.append("Reuse Keyword")
        
    if project["typologies"]:
        for t in project["typologies"]:
            if t and t.lower() in text_to_search:
                score += 20
                reasons.append(f"Typology Match ({t})")

    # Strict fallback constraints
    if not has_arch and not has_reuse:
        if not (exact_phrase_match and has_city and has_actor):
            return 0, ["Rejected: No architectural/reuse keywords and missing strict context"]
            
    if matched_words == 0 and not (has_city and has_actor):
        return 0, ["Rejected: Unrelated (No name, city, or actor match)"]

    return score, reasons

def get_base_name(raw_name):
    clean_name = re.sub(r'\(.*?\)', '', raw_name)
    parts = re.split(r'[,/]', clean_name)
    parts = [p.strip() for p in parts if len(p.strip()) > 3]
    if parts:
        return parts[0]
    return raw_name.strip()

def is_image_url(url):
    ext = Path(urlparse(url).path).suffix.lower().lstrip('.')
    return ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']

def harvest_and_review():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    projects = get_projects_context_from_neo4j()
    print(f"Found {len(projects)} projects. Building Review Lists...")
    
    for project in projects:
        proj_name = project["name"]
        safe_name = sanitize_filename(proj_name)
        proj_dir = BASE_DIR / safe_name
        proj_dir.mkdir(parents=True, exist_ok=True)
        
        md_path = proj_dir / "review_candidates.md"
        
        print(f"Processing '{proj_name}'...")
        base_name = get_base_name(proj_name)
        
        queries = [
            base_name,
            f'{base_name} architecture',
            f'{base_name} reuse'
        ]
        if project["city"]:
            queries.append(f'{base_name} {project["city"]}')
            
        queries = list(dict.fromkeys(queries))
            
        candidates_scored = []
        seen_urls = set()
        
        for query in queries:
            print(f"  Query: '{query}'")
            raw_candidates = []
            raw_candidates.extend(search_wikidata(query))
            raw_candidates.extend(search_wikimedia(query))
            raw_candidates.extend(search_openverse(query))
            
            for cand in raw_candidates:
                url = cand["url"]
                if not url or url in seen_urls: continue
                seen_urls.add(url)
                
                if not is_image_url(url): continue
                
                score, reasons = evaluate_image(cand, project)
                if score >= SCORE_THRESHOLD:
                    cand["score"] = score
                    cand["reasons"] = reasons
                    candidates_scored.append(cand)
                    
        # Sort by score descending
        candidates_scored.sort(key=lambda x: x["score"], reverse=True)
        
        if candidates_scored:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# Image Review Candidates: {proj_name}\n\n")
                f.write(f"**Location:** {project['city'] or 'Unknown'}, {project['country'] or 'Unknown'}\n")
                f.write(f"**Actors:** {', '.join(project['actors']) if project['actors'] else 'None'}\n")
                f.write(f"**Typologies:** {', '.join(project['typologies']) if project['typologies'] else 'None'}\n\n")
                f.write("---\n\n")
                
                for idx, c in enumerate(candidates_scored):
                    f.write(f"### {idx+1}. {c['title']}\n")
                    f.write(f"**Relevance Score:** {int(c['score'])}/100  \n")
                    f.write(f"**Match Reasons:** {', '.join(c['reasons'])}  \n")
                    f.write(f"**Author:** {c['author']} | **License:** {c['license']} | **Source:** {c['source']}  \n")
                    f.write(f"**[View Original Link]({c['source_link']})**\n\n")
                    
                    # Embedding Thumbnail
                    f.write(f"<img src=\"{c['thumb_url']}\" width=\"400\" />\n\n")
                    f.write("---\n")
            print(f"  -> Generated review list with {len(candidates_scored)} candidates.")
        else:
            print(f"  -> No valid candidates found above threshold.")

if __name__ == "__main__":
    harvest_and_review()