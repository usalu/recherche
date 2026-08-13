export const meta = {
  name: 'faktencheck-shard-AT',
  description: 'Live re-verification of drawn actor-network nodes/edges for AT',
  phases: [{ title: 'Shard-AT', detail: '4 agents, one evidence-clustered packet each' }],
}

const NODE_VERDICT = {
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
}
const EDGE_VERDICT = {
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
}
const SHARD_SCHEMA = {
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
}

const KRITERIEN = "GRADE (Akteure) -- in dieser Reihenfolge anwenden, beim ersten Treffer stoppen:\n  kern       Die Organisation stellt auf einer EIGENEN, heute erreichbaren Seite Wiederverwendung/\n             Zirkularitaet von Bauteilen als Teil ihres Tuns dar (Leistungsseite, Ueber-uns, Shop,\n             Depot, Programm, Institutslinie) -- DAUERHAFT platziert, nicht als News/Blog/Einzelreferenz.\n             AUSGESCHLOSSEN: einzelnes Reuse-Projekt als einzige Fundstelle; Fremdverzeichnis;\n             Recycling/Rezyklat/Abfall ohne Bauteilbezug; nur Pressemitteilung Dritter.\n  bezug      Eine oeffentliche Seite nennt die Organisation NAMENTLICH in einer BENANNTEN Reuse-Sache\n             (Projekt, Konsortium, Programm, Netzwerk mit Mitgliedspflichten).\n             AUSGESCHLOSSEN: reine Verzeichnislistung; generische Partner-/Kundennennung ohne\n             Reuse-Sache; unbestaetigte *_candidate-Ableitung.\n  ohne_beleg Verfahren (siehe unten) vollstaendig durchlaufen, keine Quelle gefunden.\n             \"ohne_beleg\" ist eine Aussage ueber die RECHERCHE, nicht ueber die Organisation --\n             fehlende oeffentliche Angaben lassen keine Rueckschluesse auf die tatsaechliche Praxis zu.\n\nBeispiele (verbindlich als Kalibrierung):\n  - SalvoWEB: betreibt Verzeichnis+Marktplatz selbst, Reuse ist Betriebszweck -> kern.\n  - CBRE bei \"55 Great Suffolk Street\": cbre.com zeigt keine Reuse-Linie, Bezug nur ueber das\n    Projekt -> bezug (NICHT kern).\n  - Gardiner & Theobald: gardiner.com/about-us ist eine Kostenplanungsseite, Reuse erscheint nicht\n    als Leistungslinie -> bezug, nicht kern.\n\nGRADE (Kanten, nur die dir zugewiesenen gezeichneten Kanten):\n  belegt              EINE Quelle nennt BEIDE Endpunkte UND die Beziehung. Zitat <=25 Woerter mit\n                      Beziehungswort (Partner, Konsortium, Tochter, uebernommen, gegruendet von,\n                      Auftraggeber, ausfuehrend). KEIN JSON-LD/CSS/Navigations-Markup als Zitat.\n  teilweise_belegt    Nur die Seite EINES Endpunkts nennt den anderen (Partner-/Referenzliste),\n                      ODER die Beziehung ist belegt, entspricht aber nicht dem gespeicherten Typ.\n  unklar              Keine Quelle nennt beide in einer REALEN Beziehung.\n                      unklar_grund: verzeichnis_only | abgeleitet | kein_fund | markup_zitat\n  REALE Beziehung = Projektpartnerschaft, Konsortialmitgliedschaft, Mutter/Tochter, Uebernahme,\n  gemeinsame Gruender, dokumentierte Betreiberschaft.\n  VERZEICHNIS-Bindungen (Opalis, bauteilnetz.de, Cirkla, Insert Marktplaats, Artisans du\n  Patrimoine, generische SalvoWEB-Listungen) sind AUSGESCHLOSSEN -> immer unklar/verzeichnis_only.\n\nFLAGS (orthogonal, beliebig viele gleichzeitig, jede braucht beleg_url):\n  nicht_pruefbar (hindernis=...) | duplikat (duplikat_von=tid des zu BEHALTENDEN) |\n  falscher_typ (typ_ist/typ_soll) | falsches_land (land_ist/land_soll, ISO2) |\n  defunkt (stand_jahr, ggf. nachfolger_tid)"
const VERFAHREN = "ENTSCHEIDUNGSABLAUF -- halte die Reihenfolge ein, damit zwei Agentinnen dasselbe Urteil erreichen:\n D1 Gespeicherte URL vorhanden (primary_source_url oder source_urls) -> abrufen. Sonst D2.\n D2 Keine URL -> ZWEI Suchen, BEIDE in such_begriffe protokollieren:\n      \"<name>\" <ort-oder-land>   und   \"<name>\" (reuse OR reclaimed OR salvage OR Wiederverwendung)\n    Hoechstens die zwei besten Treffer oeffnen. Kein plausibler Treffer (Name UND Ort muessen\n    passen) -> ohne_beleg. NIEMALS aus einer fehlenden URL im Datensatz auf Peripherie schliessen.\n D3 404/DNS tot -> einmal Domain-Wurzel probieren, dann D2-Suche nach Umzug. Gefunden -> weiter,\n    url_korrigiert notieren. Nachweislich eingestellt -> Flag defunkt + Grad aus diesem Nachweis\n    (meist bezug). Sonst nicht_pruefbar/dns_tot. EINE TOTE SEITE ERGIBT NIEMALS ohne_beleg.\n D4 403/429/Login/Paywall -> Flag nicht_pruefbar mit passendem hindernis. DANN trotzdem EINE\n    Drittquelle versuchen (Register, inhaltliches Verzeichnis, Projektseite). Traegt sie einen\n    Grad, vergib ihn UND behalte das Flag. bezug + nicht_pruefbar ist eine gueltige Kombination.\n D5 Fremdsprache -> zuerst ueber das Reuse-Lexikon der Sprache und Struktur entscheiden (Shop mit\n    gebrauchten Bauteilen, Depotadresse, \"ombruk\"/\"\u00e5terbruk\"/\"genbrug\"/\"kierr\u00e4tys\"/\"hergebruik\"/\n    \"r\u00e9emploi\"). Grad vergeben mit sprache=<iso>, sprachrisiko=true. Nur bei wirklich\n    unzugaenglichem Text (Bild-PDF, Script-Rendering) -> nicht_pruefbar/sprache.\n    SPRACHE ALLEIN IST KEIN NICHT-URTEIL.\n D6 Uebernommen/umbenannt -> den NACHFOLGER bewerten. Ist der Nachfolger selbst im Panel (siehe\n    ANDERE tids unten) -> Flag duplikat mit duplikat_von. Sonst nur Notiz in begruendung.\n D7 Grad kern -> bezug -> ohne_beleg, erstes Bestehen zaehlt.\n D8 Je Kante hoechstens 3 Werkzeugaufrufe, dann unklar/kein_fund mit budget_erschoepft=true.\n D9 Projektknoten (is_project=true): bewertet wird, ob das BAUVORHABEN Bauteil-Wiederverwendung\n    dokumentiert. Ist das \"Projekt\" in Wahrheit Person/Organisation/Programm -> Flag falscher_typ."
const EHRLICHKEIT = "HARTE REGELN -- Verstoesse machen den ganzen Durchgang wertlos:\n 1. Jeder Grad ausser ohne_beleg/unklar braucht beleg_url + beleg_zitat. Das Zitat muss WOERTLICH\n    auf der geoeffneten Seite stehen. Ein spaeterer Pruefdurchgang oeffnet deine URL erneut und\n    sucht dein Zitat -- findet er es nicht, wird dein Urteil verworfen.\n 2. Erfinde keine URL und kein Zitat. Nutze keine Seite, die du nicht selbst geoeffnet hast.\n 3. Beurteile nie nach Plausibilitaet. \"Klingt nach einem Rueckbauunternehmen\" ist kein Beleg.\n    Der Name allein traegt kein Urteil.\n 4. Zitate aus JSON-LD, CSS, Cookie-Bannern oder Navigation sind KEINE Belege.\n 5. Fehlende Belege sind keine Belege fuer Fehlen. ohne_beleg ist ein Rechercheergebnis, keine\n    Aussage ueber die Organisation.\n 6. HARTKAPPE 32 Werkzeugaufrufe insgesamt. Bei Erreichen: HOER AUF, trage jede nicht erreichte\n    tid in ungeprueft_tids ein, setze kappe_erreicht=true. Eine offen gemeldete Luecke ist richtig.\n    Ein geratenes Urteil ist ein Fehler.\n 7. Gib fuer JEDE zugewiesene tid entweder ein Urteil ODER einen Eintrag in ungeprueft_tids zurueck.\n    Die Summe muss die Zahl deiner zugewiesenen tids ergeben.\n 8. Empfiehl NICHTS zur Loeschung. Loeschkandidaten werden aus deinen Graden und Flags berechnet,\n    nicht von dir beurteilt."

phase('Shard-AT')

const _argsParsed = typeof args === 'string' ? JSON.parse(args) : args
const packets = Array.isArray(_argsParsed) ? _argsParsed : _argsParsed.packets
log(`AT: ${packets.length} packets, ${packets.reduce((n,p)=>n+p.nodes.length,0)} nodes, ` +
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
    { label: `AT:${p.packet_id}`, phase: 'Shard-AT', model: 'sonnet', effort: 'medium', schema: SHARD_SCHEMA })
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
log(`AT: ${nodes.length} Knotenurteile, ${edges.length} Kantenurteile, ${gaps.length} ungeprueft`)
log(`AT: kern=${nodes.filter(n=>n.actor_degree==='kern').length} ` +
    `bezug=${nodes.filter(n=>n.actor_degree==='bezug').length} ` +
    `ohne_beleg=${nodes.filter(n=>n.actor_degree==='ohne_beleg').length}`)

return { ccs: ["AT"], packets: ok, nodes, edges, ungeprueft: gaps, ausgefallen: lost.map(p => p.packet_id) }
