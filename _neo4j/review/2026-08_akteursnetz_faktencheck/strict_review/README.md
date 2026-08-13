# Strict Research-only Review

Dieser Ordner ist ein report-spezifischer Review-Layer. Er verändert weder
Neo4j noch die ursprünglichen Klassifikations- oder Faktencheck-Dateien.

## Ablauf

1. `build_candidates.py` friert die Eingaben per SHA-256 ein und erzeugt das
   vollständige Kandidatenregister.
2. `lane_A.json`, `lane_B.json` und `lane_C.json` enthalten genau eine
   EID-basierte Entscheidung für jeden der 859 Einträge.
3. `validate_strict_review.py` prüft Vollständigkeit, Evidenzdeckung,
   Entitätstrennung, Merge-Ziele, Namen und die unveränderten Eingaben.
4. Erst nach abgeschlossener Gegenprüfung und explizitem Setzen von
   `approved_for_render_prune` erzeugt `finalize_strict_review.py` aktive,
   report-spezifische Artefakte. Ohne Freigabe bricht der Finalizer ab.

Die finale Ausgabe trennt `Programm`-Einträge in
`programme_strict_final.json` von der Akteurs-/Projektansicht. Die
gefilterte Akteurs-/Projektdatei ist
`klassifikation_actor_project_final.json`. Die
report-spezifische Typkorrektur bleibt zusätzlich in
`report_overrides_strict.json` und `klassifikation_final.json` erhalten.

`audit_id` ist nur eine menschenlesbare Prüf-ID. Technische Joins verwenden
ausschließlich `eid`.
