"""Score candidate quotes against bg_hunt alias sets. §2.4 of hunting plan."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from html import unescape

SHORT_ALLOWLIST = {"sol", "mur", "bois", "dak", "alu", "pvc", "ver", "glas"}
# Avoid false compound-prefix hits on very short/generic stems
STEM_STOP = {"mehr", "wand", "und", "aus", "der", "die", "das", "von", "mit", "fuer", "fur", "the", "and"}


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def token_hit(alias: str, text: str) -> bool:
    """Match alias as whole word OR as leading stem inside German compounds (decke→deckenelemente)."""
    a = norm_text(alias)
    t = norm_text(text)
    if not a:
        return False
    min_len = 3 if a in SHORT_ALLOWLIST else 4
    if len(a) < min_len:
        return False
    # Whole-word match
    if re.search(r"(?<![a-z0-9äöüß])" + re.escape(a) + r"(?![a-z0-9äöüß])", t):
        return True
    # Compound prefix: alias at start of a longer token
    if len(a) >= 4 and a not in STEM_STOP:
        for word in re.findall(r"[a-z0-9äöüß]{4,}", t):
            if word.startswith(a) and len(word) > len(a):
                return True
    return False


def is_valid_quote(quote: str) -> bool:
    if not quote or len(quote.strip()) < 15:
        return False
    q = quote.strip()
    bad = ("function(", "dataLayer", "@context", "javascript", "stylesheet", "cdn/shop")
    if any(m.lower() in q.lower() for m in bad):
        return False
    # Reject raw schema property dumps (flaeche_m2: 1412 upfront_embodied...)
    if re.match(r"^[a-z][a-z0-9_]{2,}:\s*[\d.]", q, re.I):
        return False
    if q.count(":") >= 3 and re.search(r"[a-z]+_[a-z]+:\s*", q):
        return False
    alpha_words = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", q)
    return len(alpha_words) >= 2


def category_nav_cap(text: str) -> bool:
    """False-positive guard: ≥8 unrelated component types in one block."""
    nav_terms = [
        "brick", "floor", "sanitary", "roof", "window", "door", "steel", "wood",
        "carrelage", "faïence", "brique", "toiture", "fenêtre", "porte", "bois",
    ]
    hits = sum(1 for t in nav_terms if token_hit(t, norm_text(text)))
    return hits >= 8


def score_quote(
    quote: str,
    project_aliases: list[str],
    component_aliases: list[str],
    material_aliases: list[str],
    *,
    require_project: bool = True,
    target_aliases: list[str] | None = None,
) -> dict:
    q = norm_text(quote)
    if category_nav_cap(quote):
        return {
            "score": 4,
            "project_hit": False,
            "component_hit": False,
            "material_hit": False,
            "target_hit": False,
            "proven_eligible": False,
            "matched_aliases": [],
            "verdict_hint": "UNSUPPORTED",
        }

    matched: list[str] = []
    pa = 0
    for a in project_aliases:
        if token_hit(a, q):
            pa += 4
            matched.append(a)
            break
    ca = 0
    for a in component_aliases:
        if token_hit(a, q):
            ca += 3
            matched.append(a)
            break
    ma = 0
    for a in material_aliases:
        if token_hit(a, q):
            ma += 2
            matched.append(a)
            break
    ta = 0
    if target_aliases:
        for a in target_aliases:
            if token_hit(a, q):
                ta += 2
                matched.append(a)
                break

    total = pa + ca + ma + ta
    if require_project and pa == 0:
        total = min(total, 4)

    # trigram fallback on best alias phrase
    if total < 5 and pa > 0:
        for aliases in (component_aliases, material_aliases):
            for phrase in aliases:
                if len(phrase) < 12:
                    continue
                ratio = SequenceMatcher(None, norm_text(phrase), q[:300]).ratio()
                if ratio >= 0.72:
                    total = max(total, 6)
                    matched.append(f"trigram:{phrase[:30]}")
                    break

    project_hit = pa > 0
    component_hit = ca > 0
    material_hit = ma > 0
    family_hit = component_hit or material_hit or (ta > 0)
    proven_eligible = total >= 8 and project_hit and family_hit and is_valid_quote(quote)

    if proven_eligible:
        verdict_hint = "PROVEN"
    elif total >= 5 and project_hit:
        verdict_hint = "PARTIAL"
    elif total >= 5 and component_hit:
        verdict_hint = "PARTIAL"
    else:
        verdict_hint = "UNSUPPORTED"

    return {
        "score": total,
        "project_hit": project_hit,
        "component_hit": component_hit,
        "material_hit": material_hit,
        "target_hit": ta > 0,
        "proven_eligible": proven_eligible,
        "matched_aliases": list(dict.fromkeys(matched)),
        "verdict_hint": verdict_hint,
    }


def extract_best_sentence(
    page_text: str,
    project_aliases: list[str],
    component_aliases: list[str],
    material_aliases: list[str],
    target_aliases: list[str] | None = None,
) -> tuple[str, dict]:
    plain = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", page_text or "", flags=re.I | re.S)
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = re.sub(r"\s+", " ", unescape(plain)).strip()
    if not plain:
        return "", {"score": 0, "verdict_hint": "UNSUPPORTED", "matched_aliases": []}

    sentences = re.split(r"(?<=[.!?])\s+|\n+", plain)
    best_quote = ""
    best_score = -1
    best_meta: dict = {}
    for sent in sentences:
        if len(sent.strip()) < 12:
            continue
        meta = score_quote(
            sent, project_aliases, component_aliases, material_aliases,
            target_aliases=target_aliases,
        )
        if meta["score"] > best_score and is_valid_quote(sent):
            best_score = meta["score"]
            best_quote = sent.strip()[:300]
            best_meta = meta
    return best_quote, best_meta
