import os
import sys
import re
import time
import requests
from urllib.parse import quote
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
    'User-Agent': 'RecherchePageReviewAssistant/1.0 (bot@example.org) requests/2.31.0'
}
SCORE_THRESHOLD = 40  # Lower threshold for pages, as text matches are more semantic

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

def search_wikipedia(query, lang="en"):
    time.sleep(0.5)
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "utf8": "",
        "format": "json",
        "srlimit": 5
    }
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if res.status_code != 200: return []
        data = res.json().get("query", {}).get("search", [])
        
        results = []
        for item in data:
            # Clean HTML tags from snippet
            snippet = re.sub(r'<[^>]+>', '', item.get("snippet", ""))
            results.append({
                "title": item.get("title"),
                "snippet": snippet,
                "url": f"https://{lang}.wikipedia.org/wiki/{quote(item.get('title').replace(' ', '_'))}",
                "source": f"Wikipedia ({lang.upper()})"
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
        "limit": 5
    }
    try:
        res = requests.get(search_url, params=search_params, headers=HEADERS, timeout=10)
        if res.status_code != 200: return []
        entities = res.json().get("search", [])
        
        results = []
        for entity in entities:
            results.append({
                "title": entity.get("label", entity.get("id")),
                "snippet": entity.get("description", ""),
                "url": entity.get("url", f"https://www.wikidata.org/wiki/{entity.get('id')}"),
                "source": "Wikidata"
            })
        return results
    except Exception as e:
        return []

def evaluate_page(page_data, project):
    score = 0
    reasons = []
    
    text_to_search = f"{page_data['title']} {page_data['snippet']}".lower()
    
    # 1. Keywords
    arch_keywords = ['architecture', 'building', 'pavilion', 'facade', 'structure', 'architektur', 'bauwerk', 'hq', 'headquarters', 'office', 'kantoor', 'gebouw', 'huis', 'house', 'construction', 'halle', 'werkhof', 'campus']
    has_arch = any(kw in text_to_search for kw in arch_keywords)
    
    reuse_keywords = ['reuse', 'reclaimed', 'circular', 'wiederverwendung', 'recycled', 'spolia', 'bauteil', 'salvage', 'upcycling', 'zirkulär']
    has_reuse = any(kw in text_to_search for kw in reuse_keywords)

    # 2. Base Name check
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
        
    # 3. Context checks
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
        reasons.append("Architecture Context")
    if has_reuse:
        score += 35
        reasons.append("Reuse Context")

    # Strict fallback constraint: Needs some relation to name, city, or actor
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

def make_google_link(query):
    return f"https://www.google.com/search?q={quote(query)}"

def harvest_and_review():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    projects = get_projects_context_from_neo4j()
    print(f"Found {len(projects)} projects. Building Page Review Lists...")
    
    for project in projects:
        proj_name = project["name"]
        safe_name = sanitize_filename(proj_name)
        proj_dir = BASE_DIR / safe_name
        proj_dir.mkdir(parents=True, exist_ok=True)
        
        md_path = proj_dir / "research_links.md"
        print(f"Processing '{proj_name}'...")
        
        base_name = get_base_name(proj_name)
        
        queries = [base_name]
        if project["city"]: queries.append(f'{base_name} {project["city"]}')
        if project["actors"]: queries.append(f'{base_name} {project["actors"][0]}')
            
        queries = list(dict.fromkeys(queries))
        
        candidates_scored = []
        seen_urls = set()
        
        for query in queries:
            raw_candidates = []
            raw_candidates.extend(search_wikipedia(query, lang="en"))
            raw_candidates.extend(search_wikipedia(query, lang="de"))
            raw_candidates.extend(search_wikidata(query))
            
            for cand in raw_candidates:
                url = cand["url"]
                if not url or url in seen_urls: continue
                seen_urls.add(url)
                
                score, reasons = evaluate_page(cand, project)
                if score >= SCORE_THRESHOLD:
                    cand["score"] = score
                    cand["reasons"] = reasons
                    candidates_scored.append(cand)
                    
        candidates_scored.sort(key=lambda x: x["score"], reverse=True)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Project Research Links: {proj_name}\n\n")
            
            f.write("## Discovered Web Pages (Evaluated for Context)\n")
            if candidates_scored:
                for idx, c in enumerate(candidates_scored):
                    f.write(f"### {idx+1}. [{c['title']}]({c['url']})\n")
                    f.write(f"- **Relevance Score:** {int(c['score'])}/100\n")
                    f.write(f"- **Source:** {c['source']}\n")
                    f.write(f"- **Match Reasons:** {', '.join(c['reasons'])}\n")
                    f.write(f"- **Snippet:** *\"{c['snippet']}...\"*\n\n")
            else:
                f.write("*No highly relevant Wikipedia/Wikidata pages found automatically.*\n\n")
                
            f.write("---\n\n")
            f.write("## Direct Search Queries for Manual Research\n")
            f.write("Use these pre-generated Google search links to find exact architectural and reuse context.\n\n")
            
            clean_name = re.sub(r'\(.*?\)', '', proj_name).strip()
            
            f.write("### Architectural & Reuse Search\n")
            f.write(f"- [Search: {clean_name} architecture]({make_google_link(clean_name + ' architecture')})\n")
            f.write(f"- [Search: {clean_name} building reuse]({make_google_link(clean_name + ' building reuse')})\n")
            f.write(f"- [Search: {clean_name} wiederverwendung bauteile]({make_google_link(clean_name + ' wiederverwendung bauteile')})\n")
            if project["city"]:
                f.write(f"- [Search: {clean_name} {project['city']}]({make_google_link(clean_name + ' ' + project['city'])})\n")
            
            f.write("\n### Associated Engineering / Architecture Offices\n")
            if project["actors"]:
                for actor in project["actors"]:
                    if actor:
                        f.write(f"**{actor}**\n")
                        f.write(f"- [Search: {actor} {clean_name}]({make_google_link(actor + ' ' + clean_name)})\n")
                        f.write(f"- [Search: {actor} architecture office]({make_google_link(actor + ' architecture office')})\n")
            else:
                f.write("*No specific actors found in the database.*\n")

            f.write("\n### Image Specific Searches\n")
            f.write(f"- [Google Images: {clean_name} architecture](https://www.google.com/search?tbm=isch&q={quote(clean_name + ' architecture')})\n")
            f.write(f"- [Google Images: {clean_name} reuse](https://www.google.com/search?tbm=isch&q={quote(clean_name + ' reuse')})\n")

        print(f"  -> Generated research_links.md with {len(candidates_scored)} discovered pages.")

if __name__ == "__main__":
    harvest_and_review()
