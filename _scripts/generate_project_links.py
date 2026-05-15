import os
import sys
import re
from pathlib import Path
import urllib.parse

current_dir = Path(__file__).parent.resolve()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    import neo4j_env
    from neo4j import GraphDatabase
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    sys.exit(1)

BASE_DIR = Path(r"E:\recherche\_images")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name.replace('/', '_'))

def get_projects_data():
    uri, user, pwd, db = neo4j_env.resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    
    query = """
    MATCH (p:Projekt)
    WHERE p.name IS NOT NULL
    OPTIONAL MATCH (a:Akteur)-[:BETEILIGT_AN]->(p)
    OPTIONAL MATCH (p)-[:LIEGT_IN_STADT]->(s:Stadt)
    OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
    RETURN p.id AS id, p.name AS name, s.name AS city, l.name AS country, collect(DISTINCT a.name) AS actors
    """
    projects = []
    try:
        result = driver.execute_query(query, database_=db)
        for record in result.records:
            projects.append({
                "name": record["name"],
                "city": record["city"],
                "country": record["country"],
                "actors": record["actors"]
            })
    finally:
        driver.close()
    return projects

def make_google_link(query):
    return f"https://www.google.com/search?q={urllib.parse.quote(query)}"

def generate_links():
    projects = get_projects_data()
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    for proj in projects:
        proj_name = proj["name"]
        safe_name = sanitize_filename(proj_name)
        proj_dir = BASE_DIR / safe_name
        proj_dir.mkdir(parents=True, exist_ok=True)
        
        md_path = proj_dir / "research_links.md"
        
        clean_name = re.sub(r'\(.*?\)', '', proj_name).strip()
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Research Links: {proj_name}\n\n")
            f.write("Use these direct links to manually find architectural and reuse-related documentation.\n\n")
            
            f.write("## Project Searches\n")
            f.write(f"- [Search: {clean_name} architecture]({make_google_link(clean_name + ' architecture')})\n")
            f.write(f"- [Search: {clean_name} circular reuse]({make_google_link(clean_name + ' circular reuse')})\n")
            f.write(f"- [Search: {clean_name} building materials reclaimed]({make_google_link(clean_name + ' building materials reclaimed')})\n")
            
            if proj["city"]:
                f.write(f"- [Search: {clean_name} {proj['city']}]({make_google_link(clean_name + ' ' + proj['city'])})\n")
            
            f.write("\n## Associated Actors (Architectural / Engineering Offices)\n")
            if proj["actors"]:
                for actor in proj["actors"]:
                    if actor:
                        f.write(f"- **{actor}**\n")
                        f.write(f"  - [Search: {actor} {clean_name}]({make_google_link(actor + ' ' + clean_name)})\n")
                        f.write(f"  - [Search: {actor} architecture office]({make_google_link(actor + ' architecture office')})\n")
            else:
                f.write("- *No specific actors found in the database.*\n")
                
            f.write("\n## Image Search (Google Images)\n")
            f.write(f"- [Image Search: {clean_name} architecture](https://www.google.com/search?tbm=isch&q={urllib.parse.quote(clean_name + ' architecture')})\n")
            f.write(f"- [Image Search: {clean_name} reuse wiederverwendung](https://www.google.com/search?tbm=isch&q={urllib.parse.quote(clean_name + ' reuse wiederverwendung')})\n")
            
    print(f"Generated research links for {len(projects)} projects.")

if __name__ == "__main__":
    generate_links()