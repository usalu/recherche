"""Shared loader + cleaning for the actor-network plates. Import from panel generators."""
import json, io, collections

SRC = r"E:/recherche/actors_network.json"

TYPE_ABBR = {"Unternehmen": "UN", "Person": "PE", "Materialhub_Bauteilboerse": "MH",
             "Forschung_Lehre": "FL", "Oeffentliche_Institution": "OI", "Organisation": "OR",
             "NGO_Verband_Netzwerk": "NG", "Software_Tool_Anbieter": "ST",
             "Foerdergeber_Programmtraeger": "FG", "Unbekannt": "UK"}
# single-letter codes: used as the ID prefix in BOTH the graph node labels (only
# 1-2 digits + 1 letter fit the 3.5mm circles) and the tables, so one ID works
# everywhere. No collisions: U/M/F/N/I/S/O/G/X/P/E all distinct.
TYPE_LETTER = {"Unternehmen": "U", "Materialhub_Bauteilboerse": "M", "Forschung_Lehre": "F",
               "NGO_Verband_Netzwerk": "N", "Oeffentliche_Institution": "I",
               "Software_Tool_Anbieter": "S", "Organisation": "O",
               "Foerdergeber_Programmtraeger": "G", "Unbekannt": "X", "Person": "E"}
ISO = {"Schweiz": "CH", "Deutschland": "DE", "Belgien": "BE", "Niederlande": "NL",
       "Frankreich": "FR", "Vereinigtes Königreich": "GB", "Österreich": "AT",
       "Dänemark": "DK", "Liechtenstein": "LI", "Finnland": "FI", "Norwegen": "NO",
       "USA": "US", "Japan": "JP", "Schweden": "SE", "Irland": "IE", "Luxemburg": "LU",
       "Estland": "EE", "Lettland": "LV", "Litauen": "LT", "Portugal": "PT", "Spanien": "ES",
       "Polen": "PL", "Tschechien": "CZ", "Slowenien": "SI", "Slowakei": "SK",
       "Ungarn": "HU", "Kroatien": "HR", "Italien": "IT", "Rumänien": "RO", "Griechenland": "GR"}
ROLE_DE = {
    "Reuse_Zirkularitaetsberatung": "Reuse-/Zirkularitätsberatung",
    "Entwurf_Planung": "Entwurf/Planung", "Materiallieferung_Markt": "Materiallieferung/Markt",
    "Forschung_Dokumentation": "Forschung/Dokumentation", "Fachplanung_Nachweis": "Fachplanung/Nachweis",
    "Bauherr_Auftraggeber": "Bauherr/Auftraggeber", "Projektmanagement_Koordination": "Projektmgmt./Koordination",
    "Rueckbau_Bauteilernte_Logistik": "Rückbau/Bauteilernte/Logistik", "Bauausfuehrung_Fertigung": "Bauausführung/Fertigung",
    "Software_Digitalisierung": "Software/Digitalisierung",
    "Materialbroker / Reuse-Marketplace-Betreiber": "Materialbroker/Marketplace",
    "Aufbereitung_Refurbishment": "Aufbereitung/Refurbishment", "Bildung_Wissenstransfer": "Bildung/Wissenstransfer",
    "Betrieb_Nutzung": "Betrieb/Nutzung", "Oeffentliche_Hand_Foerderung": "Öffentliche Hand/Förderung",
    "Unbestimmt": "Unbestimmt", "Tragwerksplanung": "Tragwerksplanung", "Nachhaltigkeitsberatung": "Nachhaltigkeitsberatung",
    "Landschaftsplanung": "Landschaftsplanung", "TGA_Gebaeudetechnik": "TGA/Gebäudetechnik",
    "Fassade": "Fassade", "Kunst_Gestaltung": "Kunst/Gestaltung"}


def esc(s):
    s = s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")
    s = s.replace("_", r"\_").replace("#", r"\#").replace("$", r"\$").replace("~", r"\textasciitilde{}")
    s = s.replace("^", r"\textasciicircum{}").replace("{", r"\{").replace("}", r"\}")
    return s.replace("/", r"\SemioSlash{}")


def esct(s, maxlen):
    """Truncate the RAW string first, then escape — never cut a LaTeX macro in half."""
    return esc(s[:maxlen])


ISO_INV = {v: k for k, v in ISO.items()}
ROLE_INV = {v: k for k, v in ROLE_DE.items()}


class Net:
    def __init__(self, overlay=None, extra_peers=None):
        d = json.load(io.open(SRC, encoding="utf-8"))
        self.by = {n["eid"]: n for n in d["nodes"]}
        self.nodes = d["nodes"]
        self.actors = [n for n in d["nodes"] if n["labels"] == ["Akteur"]]
        R = collections.defaultdict(set); T = {}; L = {}
        part = collections.defaultdict(set); peers = collections.defaultdict(set)
        for r in d["relationships"]:
            t, s, e = r["type"], r["start"], r["end"]
            if t == "HAT_AKTEURROLLE": R[s].add(self.name(e))
            elif t == "HAT_AKTEURTYP": T[s] = self.name(e)
            elif t == "LIEGT_IN_LAND": L[s] = self.name(e)
            elif t == "BETEILIGT_AN": part[s].add(e)
            elif t == "VERBUNDEN_MIT_AKTEUR" and s != e: peers[s].add(e); peers[e].add(s)
            elif t == "BETRIEBEN_VON" and s != e: peers[s].add(e); peers[e].add(s)
        # FIX: 5 actors carry a `land` property but no LIEGT_IN_LAND edge — merge.
        self.land_fixed = 0
        for a in self.actors:
            if a["eid"] not in L and "land" in a["properties"]:
                L[a["eid"]] = a["properties"]["land"]; self.land_fixed += 1
        self.roles, self.types, self.land, self.part, self.peers = R, T, L, part, peers
        self.new_eids = set()
        if overlay:
            for ov in (overlay if isinstance(overlay, list) else [overlay]):
                self._merge_overlay(ov)
        # known<->known peer edges (e.g. second-audit findings between two actors
        # that both already existed in the base graph) -- no new node created.
        self.extra_peer_pairs = 0
        for a, b in (extra_peers or []):
            if a in self.by and b in self.by and a != b:
                self.peers[a].add(b); self.peers[b].add(a)
                self.extra_peer_pairs += 1
        # sort actors alphabetically, assign stable numbers A001..
        self.order = sorted(self.actors, key=lambda a: a["properties"]["name"].lower())
        self.aid = {a["eid"]: i + 1 for i, a in enumerate(self.order)}
        # role profiles
        self.prof = {a["eid"]: frozenset(R[a["eid"]]) for a in self.actors}
        prof_count = collections.Counter(self.prof.values())
        self.profiles = [k for k, _ in prof_count.most_common()]
        self.pid = {k: i + 1 for i, k in enumerate(self.profiles)}
        # projects (BETEILIGT_AN targets that are Projekt)
        # secondary key `e` (eid) breaks ties deterministically -- this sorts a
        # SET comprehension over `part[...]` (a defaultdict(set)) by display
        # name; two projects sharing an identical name would otherwise tie-break
        # in hash-random per-process order.
        self.projects = sorted({e for a in self.actors for e in part[a["eid"]]
                                if self.by[e]["labels"] == ["Projekt"]}, key=lambda e: (self.name(e), e))
        self.pjidx = {e: i for i, e in enumerate(self.projects)}

    def _merge_overlay(self, ov):
        if not hasattr(self, "new_proj_cc"):
            self.new_proj_cc = {}
        keymap = {}
        for ent in ov["entities"]:
            eid = "NEW:" + ent["key"]
            keymap[ent["key"]] = eid
            is_proj = ent.get("is_project", False)
            node = {"eid": eid, "labels": ["Projekt" if is_proj else "Akteur"],
                    "properties": {"id": ent["key"], "name": ent["name"]}}
            self.by[eid] = node
            self.nodes.append(node)
            if not is_proj:
                self.actors.append(node)
            self.new_eids.add(eid)
            cc_full = ISO_INV.get(ent["cc"])
            if cc_full:
                self.land[eid] = cc_full
            if is_proj and ent.get("cc"):
                self.new_proj_cc[eid] = ent["cc"]
            for r in ent.get("rollen", []):
                canon = r if r in ROLE_DE else ROLE_INV.get(r, r)
                self.roles[eid].add(canon)
            self.types[eid] = ent["typ"]
        # resolve known targets by name -> eid
        name2eid = {}
        for a in self.actors:
            name2eid.setdefault(a["properties"]["name"], a["eid"])
        for ed in ov["edges"]:
            s = keymap.get(ed["src"])
            if not s: continue
            if "to_known" in ed:
                t = name2eid.get(ed["to_known"])
            else:
                t = keymap.get(ed["to_new"])
            if not t or t == s: continue
            self.peers[s].add(t); self.peers[t].add(s)

    def name(self, e):
        return self.by[e]["properties"].get("name", "?") if e in self.by else "?"

    def typ(self, e):
        return TYPE_ABBR.get(self.types.get(e), "--")

    def iso(self, e):
        return ISO.get(self.land.get(e), "--")


if __name__ == "__main__":
    n = Net()
    print(f"actors={len(n.actors)} profiles={len(n.profiles)} projects={len(n.projects)}")
    print(f"land-property merges applied: {n.land_fixed}")
    print(f"peers touched: {len(n.peers)}")
    slash = sum(1 for a in n.actors if '/' in a['properties']['name'])
    print(f"slash-names: {slash}")
    import collections as _c
    ll = sorted(len(a['properties']['name']) for a in n.actors)
    print(f"name len p50={ll[len(ll)//2]} p90={ll[int(len(ll)*.9)]} max={ll[-1]}")
