export const meta = {
  name: 'faktencheck-verify',
  description: 'Adversarial re-check of kern verdicts and belegt edges: does the cited quote actually stand on the cited page?',
  phases: [{ title: 'Verify', detail: 'one agent per slice; each opens the cited URLs and searches for the cited quote' }],
}

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    slice: { type: 'string' },
    checks: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        kind:   { type: 'string', enum: ['node', 'edge'] },
        ref:    { type: 'string' },
        cc:     { type: 'string' },
        name:   { type: 'string' },
        url:    { type: 'string' },
        ergebnis: { type: 'string', enum: [
          'bestaetigt',              // quote stands verbatim (or trivially normalised) on the page
          'sinngemaess',             // page supports the claim but the quote is not verbatim
          'zitat_nicht_gefunden',    // page opened fine, quote is NOT on it -> verdict must be discarded
          'seite_nicht_erreichbar',  // 404/403/timeout etc -- NOT a failure of the original verdict
        ]},
        hindernis: { type: 'string', enum: ['login','paywall','bot_block','dns_tot','http_404','http_5xx','timeout','sprache','nur_bild',''] },
        gefundene_stelle: { type: 'string' },
        bemerkung: { type: 'string' },
      },
      required: ['kind','ref','url','ergebnis','bemerkung'],
    }},
    geprueft: { type: 'integer' },
    kappe_erreicht: { type: 'boolean' },
  },
  required: ['slice','checks','geprueft','kappe_erreicht'],
}

const VERDICTS = String.raw`E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\verdicts.json`

const REGELN = `DEINE AUFGABE -- du bist die Gegenprobe, nicht die Zweitmeinung.

Ein frueherer Durchgang hat Urteile mit Beleg-URL und woertlichem Beleg-Zitat vergeben.
Du pruefst AUSSCHLIESSLICH EINES: steht das Zitat wirklich auf der angegebenen Seite?

Du bewertest NICHT, ob das Urteil (kern/belegt) inhaltlich richtig war. Du suchst das Zitat.

VORGEHEN je Eintrag:
 1. beleg_url mit WebFetch oeffnen.
 2. Nach dem beleg_zitat suchen. Erlaubt sind nur triviale Abweichungen:
    Gross-/Kleinschreibung, Zeilenumbrueche, Mehrfach-Leerzeichen, typografische
    vs. gerade Anfuehrungszeichen, ... -Auslassungen, Umlaut-Umschrift (ue/ae/oe).
 3. ergebnis setzen:
    bestaetigt             Zitat steht (ggf. trivial abweichend) auf der Seite.
                           Trage die tatsaechlich gefundene Stelle in gefundene_stelle ein.
    sinngemaess            Die Seite traegt die Aussage erkennbar, das Zitat ist aber
                           NICHT woertlich so vorhanden (z. B. umformuliert, uebersetzt,
                           aus mehreren Saetzen zusammengezogen). Trage in
                           gefundene_stelle ein, was tatsaechlich dasteht.
    zitat_nicht_gefunden   Seite laedt normal, das Zitat steht nicht darauf und die Seite
                           traegt die Aussage auch nicht sinngemaess. Das ist ein BEFUND --
                           melde ihn ohne Zoegern.
    seite_nicht_erreichbar 404/403/Login/Paywall/Timeout/DNS tot. hindernis setzen.
                           Das ist KEIN Fehler des urspruenglichen Urteils.

HARTE REGELN:
 - Erfinde nichts. gefundene_stelle muss woertlich von der geoeffneten Seite stammen.
 - Sei streng: "klingt plausibel" ist nicht "steht da". Im Zweifel zitat_nicht_gefunden.
 - Sei aber fair: eine tote Seite ist seite_nicht_erreichbar, nicht zitat_nicht_gefunden.
 - Kein Urteil ohne Seitenaufruf. Wenn du die Seite nicht geoeffnet hast, ist es
   seite_nicht_erreichbar mit passendem hindernis.
 - HARTKAPPE 40 Werkzeugaufrufe. Bei Erreichen: aufhoeren, kappe_erreicht=true setzen,
   und nur die tatsaechlich geprueften Eintraege zurueckgeben.
 - Gib fuer jeden geprueften Eintrag genau einen checks-Eintrag zurueck.`

const _a = typeof args === 'string' ? JSON.parse(args) : args
const slices = _a.slices          // [{kind:'node'|'edge', start, end}, ...]

phase('Verify')
log(`Verify: ${slices.length} Scheiben, ` +
    `${slices.reduce((n,s)=>n+(s.end-s.start),0)} Belege insgesamt`)

const results = await parallel(slices.map(s => () =>
  agent(
`Du bist die adversariale Gegenprobe eines Faktenchecks zum europaeischen Akteursnetz
der Bauteil-Wiederverwendung.

SETUP:
 1. Rufe ToolSearch mit query "select:Read,WebFetch,WebSearch" auf, um Datei- und
    Web-Werkzeuge zu laden.
 2. Lies die Datei:
    ${VERDICTS}
    Sie enthaelt zwei Listen: "nodes" und "edges".
 3. DEINE SCHEIBE: nimm aus der Liste "${s.kind === 'node' ? 'nodes' : 'edges'}"
    ${s.kind === 'node'
      ? `alle Eintraege mit actor_degree == "kern"`
      : `alle Eintraege mit edge_degree == "belegt"`},
    in der Reihenfolge, in der sie in der Datei stehen, und daraus die Eintraege
    mit Index ${s.start} (einschliesslich) bis ${s.end} (ausschliesslich).
    Das sind ${s.end - s.start} Eintraege. Pruefe genau diese.

 Je Eintrag brauchst du: ${s.kind === 'node'
      ? 'tid, cc, name, beleg_url, beleg_zitat'
      : 'edge_id (als ref), cc, a_tid/b_tid, beleg_url, beleg_zitat'}.
 Setze ref = ${s.kind === 'node' ? 'tid' : 'edge_id'} und kind = "${s.kind}".

${REGELN}

slice = "${s.kind}:${s.start}-${s.end}"

Liefere das strukturierte Objekt.`,
    { label: `verify:${s.kind}:${s.start}-${s.end}`, phase: 'Verify',
      model: 'sonnet', effort: 'high', schema: VERIFY_SCHEMA })
))

const ok = results.filter(Boolean)
const checks = ok.flatMap(r => r.checks)
const n = checks.length
const by = k => checks.filter(c => c.ergebnis === k).length
const reproduzierbar = by('bestaetigt')
const pruefbar = n - by('seite_nicht_erreichbar')

log(`Verify: ${n} Belege geprueft`)
log(`  bestaetigt=${by('bestaetigt')} sinngemaess=${by('sinngemaess')} ` +
    `zitat_nicht_gefunden=${by('zitat_nicht_gefunden')} ` +
    `seite_nicht_erreichbar=${by('seite_nicht_erreichbar')}`)
log(`  Zitat-Reproduktionsrate (nur erreichbare Seiten): ` +
    `${pruefbar ? (100*reproduzierbar/pruefbar).toFixed(1) : 'n/a'}%`)

return {
  checks,
  summe: n,
  bestaetigt: by('bestaetigt'),
  sinngemaess: by('sinngemaess'),
  zitat_nicht_gefunden: by('zitat_nicht_gefunden'),
  seite_nicht_erreichbar: by('seite_nicht_erreichbar'),
  reproduktionsrate_erreichbare: pruefbar ? reproduzierbar / pruefbar : null,
  ausgefallen: slices.length - ok.length,
}
