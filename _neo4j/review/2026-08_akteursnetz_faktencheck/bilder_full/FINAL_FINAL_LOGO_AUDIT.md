# Finales Schlussaudit aller ausgewählten Logos

Erzeugt: 2026-08-16T08:21:46+00:00

## Ergebnis

- 476/476 ausgewählte Logos technisch und regelbasiert erneut geprüft.
- **289** ohne erkannte Restunsicherheit (`confirmed_exact`).
- **185** vorsorglich manuell zu prüfen (`manual_check`).
- **2** mit hoher Priorität zu prüfen (`manual_check_high`).
- **0** technische Assetfehler.
- **13** exakte Hash-Dubletten-Gruppen; jede beteiligte Zuordnung ist bewusst markiert.
- 476/476 Logos auf den 33 vollständigen Prüfbögen visuell geprüft; 187/476 markierte Grenzfälle zusätzlich auf 24 Schlussaudit-Bögen geprüft.
- 0 visuell offensichtliche Vertauschungen, Partnerlogos, Fotos oder Social-Media-Zeichen gefunden.
- `mit-bestand` unverändert; keine Neo4j-Schreiboperation.

„Manuell prüfen“ bedeutet nicht „falsch“. Die Warteschlange enthält bewusst jeden Fall mit auch nur kleiner Unsicherheit: Träger-/Nachfolgemarke, kombinierte Bezeichnung, schwächere Quellenart, abweichende Domain, Inline-Extraktion, Hash-Dublette, Transportauffälligkeit oder nicht erneut erreichbare Quelldatei.

## Hohe Priorität

- `DE:I05` — Roskilde Kommune: Das bisherige Roskilde-Apple-Touch-Asset antwortet mit HTTP 404; aktuelle Design-/Logo-Seite bitte gegenprüfen. | Schlüsselpräfix DE weicht vom Länderfeld DK ab; Overlay-/Transportzuordnung prüfen.
- `FR:M44` — PROCLUS: Die bisherige PROCLUS-Quelldatei antwortet mit HTTP 404; die offizielle Website zeigt inzwischen ein neues Logo-Asset.

## Zuletzt ergänzte Logos mit manueller Markierung

- `BE:M17` — Heyns Recycling: Quelldatei nur über unverschlüsseltes HTTP referenziert.
- `CURRENT:BE:advitam-material` — AD VITAM MATERIAL (ehem. Plateforme Réemploi): Nachfolge-/aktuelle Marke für Plateforme Réemploi; manuelle Bestätigung empfohlen. | Netzbezeichnung kombiniert Organisation, Untereinheit, Träger oder Ortszusatz. | Aktueller Overlay-Schlüssel statt eingefrorener Graph-ID; Identitätszuordnung manuell prüfen.
- `CH:U22` — Schmidiger + Rosasco AG: Netzbezeichnung kombiniert Organisation, Untereinheit, Träger oder Ortszusatz.
- `CURRENT:FR:toulousemetropole` — Toulouse Métropole: Aktueller Overlay-Schlüssel statt eingefrorener Graph-ID; Identitätszuordnung manuell prüfen.
- `FR:N02` — Bellastock: Offizielles Bellastock-Asset antwortete beim Schlusscheck mit HTTP 403; lokaler offizieller Snapshot vorhanden.
- `GB:M07` — E&A Reclamation: Quelldatei liegt auf anderer Domain (static.squarespace.com) als die offizielle Seite (eandareclamation.com).
- `GB:M09` — Enviromate: Quelldatei liegt auf anderer Domain (s3-eu-west-1.amazonaws.com) als die offizielle Seite (enviromate.co.uk).
- `GB:M21` — Surplus Building & Plumbing Materials: Deklariertes Site-Icon kann eine verkürzte Bildmarke statt des vollständigen Logos sein.
- `NL:S03` — Ter Velde & Den Besten: Offizielles Ter-Velde-&-Den-Besten-Asset antwortete beim Schlusscheck mit HTTP 403; Snapshot vorhanden.
- `NL:U33` — Lagemaat Heerde: Offizielles Lagemaat-Asset antwortete beim Schlusscheck mit HTTP 403; lokaler offizieller Snapshot vorhanden.
- `BE:S03` — Sundahus: SundaHus wird in aktueller iBinder-Gruppenfassung dargestellt. | Schlüsselpräfix BE weicht vom Länderfeld SE ab; Overlay-/Transportzuordnung prüfen.

## Manuelle Warteschlange

Die vollständige Liste der 187 markierten Logos steht in `FINAL_FINAL_LOGO_AUDIT.csv` und in der klickbaren Galerie `FINAL_FINAL_LOGO_AUDIT.html`. Die Galerie startet mit dem Filter „nur manuell“ und enthält offizielle Seite, Quelldatei, Hell-/Dunkelvorschau sowie alle Markierungsgründe.

## Rechte

Identitätsprüfung und Bildrechte bleiben getrennt. Für Veröffentlichungsfreigaben ist weiterhin `CURRENT_IMAGE_RIGHTS_AUDIT.csv` maßgeblich.
