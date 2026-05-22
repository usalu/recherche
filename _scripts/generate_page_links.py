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
    'User-Agent': 'RecherchePageReviewAssistant/1.1 (bot@example.org) requests/2.31.0'
}
SCORE_THRESHOLD = 40

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
    time.sleep(0.3)
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
            snippet = re.sub(r'<[^>]+>', '', item.get("snippet", ""))
            results.append({
                "title": item.get("title"),
                "snippet": snippet,
                "url": f"https://{lang}.wikipedia.org/wiki/{quote(item.get('title').replace(' ', '_'))}",
                "source": f"Wikipedia ({lang.upper()})"
            })
        return results
    except Exception: return []

def search_wikidata(query):
    time.sleep(0.3)
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
    except Exception: return []

def evaluate_page(page_data, project):
    score = 0
    reasons = []
    text_to_search = f"{page_data['title']} {page_data['snippet']}".lower()
    
    arch_keywords = ['architecture', 'building', 'pavilion', 'facade', 'structure', 'architektur', 'bauwerk', 'office', 'house']
    has_arch = any(kw in text_to_search for kw in arch_keywords)
    reuse_keywords = ['reuse', 'reclaimed', 'circular', 'wiederverwendung', 'recycled', 'bauteil']
    has_reuse = any(kw in text_to_search for kw in reuse_keywords)

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
        
    if project["city"] and project["city"].lower() in text_to_search:
        score += 30
        reasons.append("City Match")
        
    for actor in project["actors"]:
        if actor and len(actor)>3 and actor.lower() in text_to_search:
            score += 35
            reasons.append(f"Actor Match ({actor})")
            
    if has_arch: score += 25
    if has_reuse: score += 35

    if matched_words == 0 and not (project["city"] and project["city"].lower() in text_to_search):
        return 0, []

    return score, reasons

def get_base_name(raw_name):
    clean_name = re.sub(r'\(.*?\)', '', raw_name)
    parts = re.split(r'[,/]', clean_name)
    parts = [p.strip() for p in parts if len(p.strip()) > 3]
    return parts[0] if parts else raw_name.strip()

def make_google_link(query):
    return f"https://www.google.com/search?q={quote(query)}"

def harvest_and_review():
    projects = get_projects_context_from_neo4j()
    print(f"Updating {len(projects)} projects with GOLDEN LINKS...")
    
    for project in projects:
        proj_name = project["name"]
        safe_name = sanitize_filename(proj_name)
        proj_dir = BASE_DIR / safe_name
        proj_dir.mkdir(parents=True, exist_ok=True)
        md_path = proj_dir / "research_links.md"
        
        base_name = get_base_name(proj_name)
        queries = [base_name]
        if project["city"]: queries.append(f'{base_name} {project["city"]}')
        if project["actors"]: queries.append(f'{base_name} {project["actors"][0]}')
        queries = list(dict.fromkeys(queries))
        
        candidates_scored = []
        seen_urls = set()
        for query in queries:
            raw_candidates = []
            raw_candidates.extend(search_wikipedia(query, "en"))
            raw_candidates.extend(search_wikipedia(query, "de"))
            raw_candidates.extend(search_wikidata(query))
            for cand in raw_candidates:
                if not cand["url"] or cand["url"] in seen_urls: continue
                seen_urls.add(cand["url"])
                score, reasons = evaluate_page(cand, project)
                if score >= SCORE_THRESHOLD:
                    cand["score"] = score
                    cand["reasons"] = reasons
                    candidates_scored.append(cand)
                    
        candidates_scored.sort(key=lambda x: x["score"], reverse=True)
        
        # --- DETERMINING GOLDEN LINK ---
        best_search_query = f'"{base_name}" architecture reuse'
        if project["actors"]:
            best_search_query = f'"{base_name}" "{project["actors"][0]}"'
        
        golden_link_url = make_google_link(best_search_query)
        golden_link_text = f"Primary Search: {best_search_query}"
        
        if candidates_scored and candidates_scored[0]["score"] >= 80:
            golden_link_url = candidates_scored[0]["url"]
            golden_link_text = f"Verified Page: {candidates_scored[0]['title']} ({candidates_scored[0]['source']})"
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# {proj_name}\n\n")
            f.write(f"## 🏆 MOST IMPORTANT LINK\n")
            f.write(f"**[{golden_link_text}]({golden_link_url})**\n\n")
            f.write("---\n\n")
            
            f.write("## Discovered Web Pages (Scored)\n")
            if candidates_scored:
                for idx, c in enumerate(candidates_scored):
                    f.write(f"### {idx+1}. [{c['title']}]({c['url']})\n")
                    f.write(f"- **Relevance:** {int(c['score'])}/100 | **Source:** {c['source']}\n")
                    f.write(f"- **Reasons:** {', '.join(c['reasons'])}\n")
                    f.write(f"- **Summary:** {c['snippet']}...\n\n")
            else:
                f.write("*No automatic pages found above score threshold.*\n\n")
                
            f.write("## Manual Research Shortcuts\n")
            clean_name = re.sub(r'\(.*?\)', '', proj_name).strip()
            f.write(f"- [Search: {clean_name} architecture]({make_google_link(clean_name + ' architecture')})\n")
            f.write(f"- [Search: {clean_name} reuse]({make_google_link(clean_name + ' reuse')})\n")
            if project["city"]:
                f.write(f"- [Search: {clean_name} {project['city']}]({make_google_link(clean_name + ' ' + project['city'])})\n")
            if project["actors"]:
                for actor in project["actors"]:
                    f.write(f"- [Search: {actor} {clean_name}]({make_google_link(actor + ' ' + clean_name)})\n")
            f.write(f"- [Google Images]({make_google_link(clean_name + ' architecture')}&tbm=isch)\n")

    print("Successfully generated Golden Links for all projects.")

if __name__ == "__main__":
    harvest_and_review()
