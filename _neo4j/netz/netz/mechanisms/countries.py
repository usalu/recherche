"""Country resolution + per-country partition. Verbatim port of
netplate.Model's stage 2 (RESOLVE) and stage 3 (PARTITION), split into two
callable steps.

Country resolution: an actor's country is STATED if a LIEGT_IN_LAND edge (or
the `land` property fallback -- see data/neo4j_export.py) names one of the 29
ISO-mapped countries. Otherwise it is INFERRED if the actor participates in
exactly one project whose address text resolves to a single country (Rule A;
validated 100% against ground truth -- see project history). An actor with
neither is UNPLACED.

Partition: of the resolved countries, only WHITELIST (DACH + established
reuse-pioneer countries) get a drawn panel. A panel is {actors, projects,
edges} for that country; edges are peer/participation ties where BOTH
endpoints are drawn actors in the same panel, de-duplicated globally (an edge
is "claimed" by whichever country panel is built first in `self.countries`
order) via a shared `drawn` set across all panels.
"""
import re
import collections
from dataclasses import dataclass, field

from ..data._identity import ISO

WHITELIST = {"CH", "DE", "AT", "BE", "NL", "FR", "GB", "DK", "SE", "NO", "FI"}

CC_TEXT = {"UK": "GB", "United Kingdom": "GB", "England": "GB", "London": "GB",
           "Schweiz": "CH", "Switzerland": "CH", "Suisse": "CH",
           "Deutschland": "DE", "Germany": "DE", "Belgium": "BE", "Belgique": "BE",
           "België": "BE", "Belgien": "BE", "Netherlands": "NL", "Nederland": "NL",
           "Niederlande": "NL", "France": "FR", "Frankreich": "FR", "Austria": "AT",
           "Österreich": "AT", "Denmark": "DK", "Danmark": "DK", "Dänemark": "DK",
           "Finland": "FI", "Finnland": "FI", "Norway": "NO", "Norwegen": "NO",
           "USA": "US", "United States": "US", "Japan": "JP", "Luxembourg": "LU",
           "Italia": "IT", "Italy": "IT", "Spain": "ES"}
CC_CITY = {"Zürich": "CH", "Basel": "CH", "Winterthur": "CH", "Genève": "CH", "Lausanne": "CH",
           "Bern": "CH", "Berlin": "DE", "Hannover": "DE", "Bremen": "DE", "Kassel": "DE",
           "München": "DE", "Brussel": "BE", "Bruxelles": "BE", "Dilbeek": "BE",
           "Anderlecht": "BE", "Gent": "BE", "Amsterdam": "NL", "Utrecht": "NL",
           "Rotterdam": "NL", "Leiden": "NL", "Eindhoven": "NL", "Maassluis": "NL",
           "Oegstgeest": "NL", "Colombelles": "FR", "Stains": "FR", "Paris": "FR",
           "Wien": "AT", "Copenhagen": "DK", "København": "DK", "Tampere": "FI",
           "Kamikatsu": "JP"}


def cc_from_text(t):
    if not t:
        return None
    for k, v in CC_TEXT.items():
        if re.search(r"\b" + re.escape(k) + r"\b", t, re.I):
            return v
    for k, v in CC_CITY.items():
        if re.search(re.escape(k), t, re.I):
            return v
    return None


def is_person(raw, e):
    return raw.types.get(e) == "Person"


@dataclass
class CountryResolution:
    cc: dict                 # eid -> ISO2 (stated or inferred)
    inferred: set             # eids resolved via single-project-country inference
    proj_cc: dict              # project eid -> ISO2 (incl. harvested new_proj_cc)
    unplaced: list              # sorted(aset - cc.keys())


def resolve_countries(raw, aset: set, new_proj_cc: dict) -> CountryResolution:
    proj_cc = {e: cc_from_text(raw.by[e]["properties"].get("adresse", "")) for e in raw.projects}
    for e, cc in new_proj_cc.items():
        proj_cc[e] = cc

    # stated: ISO.get(land-name, "--") for every aset member with a land entry
    # ("--" for an unmapped land name is a legacy quirk, preserved for parity
    # -- it never survives the WHITELIST filter downstream).
    cc = {e: ISO.get(raw.land.get(e), "--") for e in aset if e in raw.land}

    inferred = set()
    for a in raw.actors:
        e = a["eid"]
        if e not in aset or e in cc:
            continue
        cs = {proj_cc[x] for x in raw.part[e] if proj_cc.get(x)}
        if len(cs) == 1:
            cc[e] = next(iter(cs))
            inferred.add(e)

    unplaced = sorted(aset - set(cc))
    return CountryResolution(cc=cc, inferred=inferred, proj_cc=proj_cc, unplaced=unplaced)


def whitelist_countries(res: CountryResolution) -> list:
    """Countries with a drawn panel, ranked by stated+inferred actor count
    (descending), country code as a deterministic tiebreak."""
    present = {c for c in res.cc.values()} | {c for c in res.proj_cc.values() if c}
    return sorted(
        (c for c in present if c in WHITELIST),
        key=lambda c: (-sum(1 for v in res.cc.values() if v == c), c),
    )


@dataclass
class Panel:
    country: str
    actors: list     # eids, sorted
    projects: list    # eids, sorted
    edges: list        # [(a, b), ...] canonically ordered, globally de-duplicated


def partition(raw, res: CountryResolution, countries: list, aset: set) -> dict:
    """Builds one Panel per whitelisted country. Edges are globally
    de-duplicated across ALL panels via a shared `drawn` set -- an edge whose
    both endpoints could belong to more than one panel (should not normally
    happen, since an actor has one country) is claimed by whichever panel is
    built first, in `countries` order."""
    panels = {}
    drawn = set()
    for c in countries:
        A = sorted(e for e, v in res.cc.items() if v == c and not is_person(raw, e))
        P = sorted(e for e, v in res.proj_cc.items() if v == c)
        inside = set(A) | set(P)
        E = []
        for e in A:
            for q in sorted(raw.peers[e]):
                if q in inside and q in aset:
                    k = (min(e, q), max(e, q))
                    if k not in drawn:
                        drawn.add(k); E.append(k)
            for x in sorted(raw.part[e]):
                if x in inside:
                    k = (e, x)
                    if k not in drawn:
                        drawn.add(k); E.append(k)
        panels[c] = Panel(country=c, actors=A, projects=P, edges=E)
    return panels, drawn


def cross_border_edges(raw, aset: set, res: CountryResolution, drawn: set) -> list:
    """Cross-border / out-of-panel edges: listed once, never drawn (parity
    with netplate.Model.cross)."""
    cross = []
    for e in aset:
        for q in raw.peers[e]:
            if q in aset:
                k = (min(e, q), max(e, q))
                if k not in drawn:
                    cross.append(("peer",) + k)
        for x in raw.part[e]:
            if x in res.proj_cc and (e, x) not in drawn:
                cross.append(("proj", e, x))
    return sorted(set(cross))
