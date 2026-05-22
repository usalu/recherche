# Einführung

- Dieses Dokument stellt einen strukturierten Mechanismus vor, um unterschiedliche Arten von Materialinformationen in nutzbare Bauteildatensätze zu überführen.

- Der Workflow folgt fünf zentralen Schritten:
  - **Raw Extraction** — Erfassen aller sichtbaren oder beschriebenen Informationen aus der Quelle.
  - **Normalization** — Vereinheitlichen von Werten, Einheiten, Bezeichnungen und Abmessungen.
  - **Classification** — Zuordnen des Bauteils zu Material-, Bauteil-, Struktur- und Wiederverwendungskategorien.
  - **Schema Mapping** — Übertragen der bereinigten Daten in datenbankfähige Felder.
  - **Human Review** — Markieren unsicherer Werte, Risiken und Prüfpunkte, die fachlich validiert werden müssen.

- Der Mechanismus wird anhand von drei Beispiel-Szenarien getestet:
  - **Szenario A:** Projekt mit umfangreichen Daten und technischer Dokumentation.
  - **Szenario B:** Begrenzte Informationen aus wenigen Bildern und einer kurzen Beschreibung.
  - **Szenario C:** Nur Prompt-/Textbeschreibung ohne zusätzliche Dokumente.

- Die Beispiele zeigen, wie derselbe Workflow mit unterschiedlichen Detailgraden, Unsicherheiten und Quellenqualitäten umgehen kann.
