"""Generates one Workflow-tool script per shard run, all from ONE embedded
criteria/procedure template, so the prompt text an agent sees is byte-
identical across every shard -- reproducibility (plan verification step 1,
the blind control set) depends on this. Never hand-edit the generated .js
files; edit this file and regenerate.

The Workflow tool has no filesystem access at runtime ("No filesystem or
Node.js API access"), so packet data cannot be read from worklist.json
inside the script -- it must travel through Workflow's `args` parameter.
This script's job is only to emit static .js text; the caller is
responsible for passing the right packets as `args` when invoking Workflow.

Usage: python gen_shard_script.py GB          -> writes shard_GB.js
       python gen_shard_script.py DK SE       -> writes shard_DK-SE.js
       python gen_shard_script.py --verify    -> writes verify.js
"""
import sys, os, json

HERE = os.path.dirname(os.path.abspath(__file__))

CAP_PER_AGENT = 32
CAP_PER_EDGE = 3

NODE_VERDICT_SCHEMA = """{
  type: 'object', additionalProperties: false,
  properties: {
    tid:   { type: 'string' },
    name:  { type: 'string' },
    actor_degree: { type: 'string', enum: ['kern', 'bezug', 'ohne_beleg'] },
    beleg_url:    { type: 'string' },
    beleg_zitat:  { type: 'string' },
    abrufdatum:   { type: 'string' },
    such_begriffe: { type: 'array', items: { type: 'string' } },
    geprueft_urls: { type: 'array', items: { type: 'string' } },
    begruendung:  { type: 'string' },
    flags: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        flag: { type: 'string', enum: ['nicht_pruefbar','duplikat','falscher_typ','falsches_land','defunkt'] },
        hindernis: { type: 'string', enum: ['login','paywall','bot_block','dns_tot','http_404','http_5xx','timeout','sprache','nur_bild',''] },
        duplikat_von: { type: 'string' },
        typ_ist: { type: 'string' }, typ_soll: { type: 'string' },
        land_ist: { type: 'string' }, land_soll: { type: 'string' },
        stand_jahr: { type: 'string' }, nachfolger_tid: { type: 'string' },
        beleg_url: { type: 'string' }, beleg_zitat: { type: 'string' },
      },
      required: ['flag','beleg_url'],
    }},
    sprache: { type: 'string' },
    sprachrisiko: { type: 'boolean' },
    budget_erschoepft: { type: 'boolean' },
  },
  required: ['tid','actor_degree','beleg_url','beleg_zitat','abrufdatum',
             'such_begriffe','geprueft_urls','begruendung','flags','budget_erschoepft'],
}"""

EDGE_VERDICT_SCHEMA = """{
  type: 'object', additionalProperties: false,
  properties: {
    edge_id: { type: 'string' },
    a_tid: { type: 'string' }, b_tid: { type: 'string' },
    edge_degree: { type: 'string', enum: ['belegt','teilweise_belegt','unklar'] },
    unklar_grund: { type: 'string', enum: ['verzeichnis_only','abgeleitet','kein_fund','markup_zitat',''] },
    relation_ist:  { type: 'string' },
    relation_soll: { type: 'string', enum: ['PROJEKT_PARTNER','KONSORTIUM','KONZERN','UEBERNAHME','GRUENDER','BETREIBER','VERZEICHNIS','KEINE',''] },
    beleg_url: { type: 'string' }, beleg_zitat: { type: 'string' }, abrufdatum: { type: 'string' },
    beide_genannt: { type: 'boolean' },
    budget_erschoepft: { type: 'boolean' },
  },
  required: ['edge_id','a_tid','b_tid','edge_degree','unklar_grund','beleg_url','beleg_zitat','beide_genannt','budget_erschoepft'],
}"""

SHARD_SCHEMA = """{
  type: 'object', additionalProperties: false,
  properties: {
    packet_id: { type: 'string' },
    nodes: { type: 'array', items: NODE_VERDICT },
    edges: { type: 'array', items: EDGE_VERDICT },
    ungeprueft_tids: { type: 'array', items: { type: 'string' } },
    tool_calls_used: { type: 'integer' },
    kappe_erreicht: { type: 'boolean' },
  },
  required: ['packet_id','nodes','edges','ungeprueft_tids','tool_calls_used','kappe_erreicht'],
}"""

VERIFY_SCHEMA = """{
  type: 'object', additionalProperties: false,
  properties: {
    checks: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        tid: { type: 'string' },
        subjekt: { type: 'string', enum: ['knoten','kante'] },
        edge_id: { type: 'string' },
        urteil: { type: 'string', enum: ['bestaetigt','herabgestuft','nicht_reproduzierbar'] },
        neuer_grad: { type: 'string', enum: ['kern','bezug','ohne_beleg','belegt','teilweise_belegt','unklar',''] },
        zitat_gefunden: { type: 'boolean' },
        befund: { type: 'string' },
        abrufdatum: { type: 'string' },
      },
      required: ['tid','subjekt','urteil','zitat_gefunden','befund','abrufdatum'],
    }},
    nicht_erreicht: { type: 'array', items: { type: 'string' } },
  },
  required: ['checks','nicht_erreicht'],
}"""

# region CriteriaText
# 🧭 THE canonical criteria text. Every shard script embeds this verbatim --
# do not paraphrase per-country. Matches plan file section "The criteria" and
# the design notes' worked examples exactly.
KRITERIEN = r"""GRADE (Akteure) -- in dieser Reihenfolge anwenden, beim ersten Treffer stoppen:
  kern       Die Organisation stellt auf einer EIGENEN, heute erreichbaren Seite Wiederverwendung/
             Zirkularitaet von Bauteilen als Teil ihres Tuns dar (Leistungsseite, Ueber-uns, Shop,
             Depot, Programm, Institutslinie) -- DAUERHAFT platziert, nicht als News/Blog/Einzelreferenz.
             AUSGESCHLOSSEN: einzelnes Reuse-Projekt als einzige Fundstelle; Fremdverzeichnis;
             Recycling/Rezyklat/Abfall ohne Bauteilbezug; nur Pressemitteilung Dritter.
  bezug      Eine oeffentliche Seite nennt die Organisation NAMENTLICH in einer BENANNTEN Reuse-Sache
             (Projekt, Konsortium, Programm, Netzwerk mit Mitgliedspflichten).
             AUSGESCHLOSSEN: reine Verzeichnislistung; generische Partner-/Kundennennung ohne
             Reuse-Sache; unbestaetigte *_candidate-Ableitung.
  ohne_beleg Verfahren (siehe unten) vollstaendig durchlaufen, keine Quelle gefunden.
             "ohne_beleg" ist eine Aussage ueber die RECHERCHE, nicht ueber die Organisation --
             fehlende oeffentliche Angaben lassen keine Rueckschluesse auf die tatsaechliche Praxis zu.

Beispiele (verbindlich als Kalibrierung):
  - SalvoWEB: betreibt Verzeichnis+Marktplatz selbst, Reuse ist Betriebszweck -> kern.
  - CBRE bei "55 Great Suffolk Street": cbre.com zeigt keine Reuse-Linie, Bezug nur ueber das
    Projekt -> bezug (NICHT kern).
  - Gardiner & Theobald: gardiner.com/about-us ist eine Kostenplanungsseite, Reuse erscheint nicht
    als Leistungslinie -> bezug, nicht kern.

GRADE (Kanten, nur die dir zugewiesenen gezeichneten Kanten):
  belegt              EINE Quelle nennt BEIDE Endpunkte UND die Beziehung. Zitat <=25 Woerter mit
                      Beziehungswort (Partner, Konsortium, Tochter, uebernommen, gegruendet von,
                      Auftraggeber, ausfuehrend). KEIN JSON-LD/CSS/Navigations-Markup als Zitat.
  teilweise_belegt    Nur die Seite EINES Endpunkts nennt den anderen (Partner-/Referenzliste),
                      ODER die Beziehung ist belegt, entspricht aber nicht dem gespeicherten Typ.
  unklar              Keine Quelle nennt beide in einer REALEN Beziehung.
                      unklar_grund: verzeichnis_only | abgeleitet | kein_fund | markup_zitat
  REALE Beziehung = Projektpartnerschaft, Konsortialmitgliedschaft, Mutter/Tochter, Uebernahme,
  gemeinsame Gruender, dokumentierte Betreiberschaft.
  VERZEICHNIS-Bindungen (Opalis, bauteilnetz.de, Cirkla, Insert Marktplaats, Artisans du
  Patrimoine, generische SalvoWEB-Listungen) sind AUSGESCHLOSSEN -> immer unklar/verzeichnis_only.

FLAGS (orthogonal, beliebig viele gleichzeitig, jede braucht beleg_url):
  nicht_pruefbar (hindernis=...) | duplikat (duplikat_von=tid des zu BEHALTENDEN) |
  falscher_typ (typ_ist/typ_soll) | falsches_land (land_ist/land_soll, ISO2) |
  defunkt (stand_jahr, ggf. nachfolger_tid)"""

VERFAHREN = r"""ENTSCHEIDUNGSABLAUF -- halte die Reihenfolge ein, damit zwei Agentinnen dasselbe Urteil erreichen:
 D1 Gespeicherte URL vorhanden (primary_source_url oder source_urls) -> abrufen. Sonst D2.
 D2 Keine URL -> ZWEI Suchen, BEIDE in such_begriffe protokollieren:
      "<name>" <ort-oder-land>   und   "<name>" (reuse OR reclaimed OR salvage OR Wiederverwendung)
    Hoechstens die zwei besten Treffer oeffnen. Kein plausibler Treffer (Name UND Ort muessen
    passen) -> ohne_beleg. NIEMALS aus einer fehlenden URL im Datensatz auf Peripherie schliessen.
 D3 404/DNS tot -> einmal Domain-Wurzel probieren, dann D2-Suche nach Umzug. Gefunden -> weiter,
    url_korrigiert notieren. Nachweislich eingestellt -> Flag defunkt + Grad aus diesem Nachweis
    (meist bezug). Sonst nicht_pruefbar/dns_tot. EINE TOTE SEITE ERGIBT NIEMALS ohne_beleg.
 D4 403/429/Login/Paywall -> Flag nicht_pruefbar mit passendem hindernis. DANN trotzdem EINE
    Drittquelle versuchen (Register, inhaltliches Verzeichnis, Projektseite). Traegt sie einen
    Grad, vergib ihn UND behalte das Flag. bezug + nicht_pruefbar ist eine gueltige Kombination.
 D5 Fremdsprache -> zuerst ueber das Reuse-Lexikon der Sprache und Struktur entscheiden (Shop mit
    gebrauchten Bauteilen, Depotadresse, "ombruk"/"återbruk"/"genbrug"/"kierrätys"/"hergebruik"/
    "réemploi"). Grad vergeben mit sprache=<iso>, sprachrisiko=true. Nur bei wirklich
    unzugaenglichem Text (Bild-PDF, Script-Rendering) -> nicht_pruefbar/sprache.
    SPRACHE ALLEIN IST KEIN NICHT-URTEIL.
 D6 Uebernommen/umbenannt -> den NACHFOLGER bewerten. Ist der Nachfolger selbst im Panel (siehe
    ANDERE tids unten) -> Flag duplikat mit duplikat_von. Sonst nur Notiz in begruendung.
 D7 Grad kern -> bezug -> ohne_beleg, erstes Bestehen zaehlt.
 D8 Je Kante hoechstens %d Werkzeugaufrufe, dann unklar/kein_fund mit budget_erschoepft=true.
 D9 Projektknoten (is_project=true): bewertet wird, ob das BAUVORHABEN Bauteil-Wiederverwendung
    dokumentiert. Ist das "Projekt" in Wahrheit Person/Organisation/Programm -> Flag falscher_typ.""" % CAP_PER_EDGE

EHRLICHKEIT = r"""HARTE REGELN -- Verstoesse machen den ganzen Durchgang wertlos:
 1. Jeder Grad ausser ohne_beleg/unklar braucht beleg_url + beleg_zitat. Das Zitat muss WOERTLICH
    auf der geoeffneten Seite stehen. Ein spaeterer Pruefdurchgang oeffnet deine URL erneut und
    sucht dein Zitat -- findet er es nicht, wird dein Urteil verworfen.
 2. Erfinde keine URL und kein Zitat. Nutze keine Seite, die du nicht selbst geoeffnet hast.
 3. Beurteile nie nach Plausibilitaet. "Klingt nach einem Rueckbauunternehmen" ist kein Beleg.
    Der Name allein traegt kein Urteil.
 4. Zitate aus JSON-LD, CSS, Cookie-Bannern oder Navigation sind KEINE Belege.
 5. Fehlende Belege sind keine Belege fuer Fehlen. ohne_beleg ist ein Rechercheergebnis, keine
    Aussage ueber die Organisation.
 6. HARTKAPPE %d Werkzeugaufrufe insgesamt. Bei Erreichen: HOER AUF, trage jede nicht erreichte
    tid in ungeprueft_tids ein, setze kappe_erreicht=true. Eine offen gemeldete Luecke ist richtig.
    Ein geratenes Urteil ist ein Fehler.
 7. Gib fuer JEDE zugewiesene tid entweder ein Urteil ODER einen Eintrag in ungeprueft_tids zurueck.
    Die Summe muss die Zahl deiner zugewiesenen tids ergeben.
 8. Empfiehl NICHTS zur Loeschung. Loeschkandidaten werden aus deinen Graden und Flags berechnet,
    nicht von dir beurteilt.""" % CAP_PER_AGENT
# endregion CriteriaText


def gen_shard(ccs, agents_hint):
    label = "-".join(ccs)
    meta_name = "faktencheck-shard-%s" % label
    return r'''export const meta = {
  name: '%(meta_name)s',
  description: 'Live re-verification of drawn actor-network nodes/edges for %(label)s',
  phases: [{ title: 'Shard-%(label)s', detail: '%(agents_hint)s agents, one evidence-clustered packet each' }],
}

const NODE_VERDICT = %(node_schema)s
const EDGE_VERDICT = %(edge_schema)s
const SHARD_SCHEMA = %(shard_schema)s

const KRITERIEN = %(kriterien)s
const VERFAHREN = %(verfahren)s
const EHRLICHKEIT = %(ehrlichkeit)s

phase('Shard-%(label)s')

const _argsParsed = typeof args === 'string' ? JSON.parse(args) : args
const packets = Array.isArray(_argsParsed) ? _argsParsed : _argsParsed.packets
log(`%(label)s: ${packets.length} packets, ${packets.reduce((n,p)=>n+p.nodes.length,0)} nodes, ` +
    `${packets.reduce((n,p)=>n+p.edges.length,0)} edges`)

const results = await parallel(packets.map(p => () =>
  agent(
`Du pruefst einen Ausschnitt eines europaeischen Akteursnetzes zur Bauteil-Wiederverwendung live
im Web nach. Ausschliesslich oeffentliche Quellen. Erhebungsstand: heutiges Datum.

SETUP: rufe ToolSearch mit query "select:WebSearch,WebFetch" auf, um die Web-Werkzeuge zu laden.

${KRITERIEN}

${VERFAHREN}

${EHRLICHKEIT}

DEIN PAKET (packet_id ${p.packet_id}, Land ${p.cc}, Art ${p.kind}):
${JSON.stringify(p.nodes, null, 1)}

ZUGEWIESENE GEZEICHNETE KANTEN:
${JSON.stringify(p.edges, null, 1)}

VORENTSCHEIDUNGEN AUS DER DATENLAGE (bereits gesetzt -- nur mit einer Nicht-Verzeichnis-Quelle
ueberstimmbar):
${JSON.stringify(p.edges.filter(e => e.vorentscheidung).map(e => ({edge_id: e.edge_id, ...e.vorentscheidung})), null, 1)}

Liefere das strukturierte Objekt. ${p.nodes.length} Knoten, ${p.edges.length} Kanten.`,
    { label: `%(label)s:${p.packet_id}`, phase: 'Shard-%(label)s', model: 'sonnet', effort: 'medium', schema: SHARD_SCHEMA })
    .then(r => r ? { ...r, packet_id: p.packet_id, cc: p.cc,
                            assigned_nodes: p.nodes.map(n => n.tid),
                            assigned_edges: p.edges.map(e => e.edge_id) } : null)
))

const ok = results.filter(Boolean)
const lost = packets.filter(p => !ok.some(r => r.packet_id === p.packet_id))
if (lost.length) log(`AUSGEFALLEN (kein Ergebnis): ${lost.map(p=>p.packet_id).join(', ')} -- ` +
                     `${lost.reduce((n,p)=>n+p.nodes.length,0)} Knoten bleiben ungeprueft`)

const nodes = ok.flatMap(r => r.nodes.map(n => ({...n, cc: r.cc, packet_id: r.packet_id})))
const edges = ok.flatMap(r => r.edges.map(e => ({...e, cc: r.cc, packet_id: r.packet_id})))
const gaps  = ok.flatMap(r => r.ungeprueft_tids).concat(lost.flatMap(p => p.nodes.map(n => n.tid)))
log(`%(label)s: ${nodes.length} Knotenurteile, ${edges.length} Kantenurteile, ${gaps.length} ungeprueft`)
log(`%(label)s: kern=${nodes.filter(n=>n.actor_degree==='kern').length} ` +
    `bezug=${nodes.filter(n=>n.actor_degree==='bezug').length} ` +
    `ohne_beleg=${nodes.filter(n=>n.actor_degree==='ohne_beleg').length}`)

return { ccs: %(ccs_json)s, packets: ok, nodes, edges, ungeprueft: gaps, ausgefallen: lost.map(p => p.packet_id) }
''' % {
        "meta_name": meta_name, "label": label, "agents_hint": agents_hint,
        "node_schema": NODE_VERDICT_SCHEMA, "edge_schema": EDGE_VERDICT_SCHEMA, "shard_schema": SHARD_SCHEMA,
        "kriterien": json.dumps(KRITERIEN), "verfahren": json.dumps(VERFAHREN), "ehrlichkeit": json.dumps(EHRLICHKEIT),
        "ccs_json": json.dumps(ccs),
    }


def gen_verify():
    return r'''export const meta = {
  name: 'faktencheck-verify',
  description: 'Adversarial re-check of every kern verdict and every belegt edge',
  phases: [{ title: 'Verify' }],
}

const VERIFY_SCHEMA = %(verify_schema)s
const KRITERIEN = %(kriterien)s

phase('Verify')
const _argsParsed = typeof args === 'string' ? JSON.parse(args) : args
const claims = Array.isArray(_argsParsed) ? _argsParsed : _argsParsed.claims
log(`verify: ${claims.length} claims (kern nodes + belegt edges)`)

function chunk(arr, n) {
  const out = []
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n))
  return out
}
const groups = chunk(claims, Math.max(1, Math.ceil(claims.length / 15)))

const out = await parallel(groups.map((g, i) => () => agent(
`Du pruefst Behauptungen ANDERER Agentinnen adversarisch nach. Du siehst nur die Behauptung und
die zitierte URL/das Zitat -- NICHT die urspruengliche Begruendung. Oeffne jede URL selbst neu.

 - Steht das behauptete Zitat WOERTLICH auf der Seite? zitat_gefunden=true/false.
 - Traegt die Seite den behaupteten Grad nach den Kriterien unten? Wenn nicht: herabstufen
   (urteil=herabgestuft, neuer_grad=<niedrigerer Grad>).
 - Ist die URL tot oder gesperrt: urteil=nicht_reproduzierbar (KEINE Herabstufung -- die
   Behauptung bleibt offen, nicht widerlegt).

Ein falsches "kern" oder "belegt" ist der teuerste Fehler dieses Projekts. Stufe im Zweifel herab.

${KRITERIEN}

BEHAUPTUNGEN:
${JSON.stringify(g, null, 1)}`,
  { label: `verify-${i}`, phase: 'Verify', model: 'opus', effort: 'high', schema: VERIFY_SCHEMA })
))

const ok = out.filter(Boolean)
const checks = ok.flatMap(r => r.checks)
const nichtErreicht = ok.flatMap(r => r.nicht_erreicht)
log(`verify: ${checks.length} checks, bestaetigt=${checks.filter(c=>c.urteil==='bestaetigt').length} ` +
    `herabgestuft=${checks.filter(c=>c.urteil==='herabgestuft').length} ` +
    `nicht_reproduzierbar=${checks.filter(c=>c.urteil==='nicht_reproduzierbar').length}`)

return { checks, nicht_erreicht: nichtErreicht }
''' % {"verify_schema": VERIFY_SCHEMA, "kriterien": json.dumps(KRITERIEN)}


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv == ["--verify"]:
        path = os.path.join(HERE, "verify.js")
        open(path, "w", encoding="utf-8", newline="\n").write(gen_verify())
        print("wrote", path)
    else:
        ccs = argv
        wl = json.load(open(os.path.join(HERE, "worklist.json"), encoding="utf-8"))
        n_packets = sum(1 for p in wl["packets"] if p["cc"] in ccs)
        script = gen_shard(ccs, n_packets)
        path = os.path.join(HERE, "shard_%s.js" % "-".join(ccs))
        open(path, "w", encoding="utf-8", newline="\n").write(script)
        print("wrote", path, "(%d packets)" % n_packets)
