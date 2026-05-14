import sys, pathlib
ROOT = pathlib.Path(r'e:/recherche')
sys.path.insert(0, str(ROOT / '_migration'))

# Simulate what the batch does
import re, unicodedata

UNCERTAIN_VALUES = {
    "", "-", "--", "---", "?", "unbekannt", "unklar", "keine quelle",
    "nicht zutreffend", "n/a", "keine", "\u2014",
}

def normalized(value):
    value = value or ""
    value = value.replace("\u00df", "ss").replace("\u00f8", "o").replace("\u00d8", "O")
    value = value.replace("\u00e6", "ae").replace("\u00c6", "AE")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    return re.sub(r"\s+", " ", value).strip()

def parse_simple_frontmatter(markdown):
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data

PRUEFUNG_RULES = [
    ("pruefung_nachweis/CE_Kennzeichnung", ("ce-markierung", "ce markierung", "ce kennzeichnung", "ce marked", "ce marking", "en 1090", "en1090")),
    ("pruefung_nachweis/Statiknachweis", ("statiknachweis", "statische prufung", "structural assessment", "tragfah", "statik", "ingenieur")),
]

# Test with actual file
p = next((ROOT / '_database/reuse_einsatz').rglob('index.md'))
md = p.read_text(encoding='utf-8', errors='replace')
fm = parse_simple_frontmatter(md)
raw = fm.get("pruefung_label", "")
print("raw pruefung_label:", repr(raw))
print("normalized:", repr(normalized(raw)))
print("is_uncertain:", normalized(raw) in UNCERTAIN_VALUES)

for segment in re.split(r"[,;]+", raw):
    seg = normalized(segment)
    print("  segment:", repr(seg))
    for target, tokens in PRUEFUNG_RULES:
        for token in tokens:
            if token in seg:
                print(f"    MATCH: {target} via token {token!r}")
