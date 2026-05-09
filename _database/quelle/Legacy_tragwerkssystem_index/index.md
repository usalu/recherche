---
entity: "quelle"
id: "Legacy_tragwerkssystem_index"
title: "Tragwerkssysteme – Index"
build_status: "promoted_phase42"
node_kind: "source"
legacy_type: "Tragwerkssystem"
---

# Tragwerkssysteme – Index

## Legacy Content

# Tragwerkssysteme – Index

## Verknüpfungen

- [bauteil/](../bauteil/) – Tragwerkssysteme bestehen aus Bauteilen; Skelettbau aus Stützen und Trägern, Betonfertigteil-System aus Wandtafeln und Deckenplatten, Dachtragwerk aus Pfetten und Bindern.
- [verbindung/](../verbindung/) – Die Reversibilität eines Systems hängt von seiner Verbindungstechnik ab: geschraubte Stahlknoten sind lösbar, vergossene Fertigteilfugen nicht.
- [reuse_strategie/](../reuse_strategie/) – Tragwerkssysteme prägen die Strategie: Skelettbau → Weiterbauen und Umnutzung; Massivbau → in-situ-Erhalt oder Bauteilrecycling; DfD-System → direkte Wiederverwendung.
- [methode/](../methode/) – Design for Disassembly und Reversibilität als Methode sind in dieser Kategorie auf Systemebene abgebildet.
- [pruefung/](../pruefung/) – Systemprüfungen: Statische Nachweisführung für das Gesamtsystem, Brandnachweis für raumabschließende Systeme, Geometrische Vermessung für Passfähigkeit.
- [fallstudie/](../fallstudie/) – Fallstudien zeigen Systeme in der Praxis: BIZH-Reallabor, CRCLR House, Be Ware und Halle 2 als Beispiele für verschiedene Systemtypen.

## Zentrale Unterthemen

- **Skelettbauweisen:** Stahl, Holz und Betonfertigteil als demontierfreundliche Primärtragwerkstypen.
- **Flächentragwerke:** Tragende Wand als massivbauorientierte Alternative; weniger rückbaubar, aber im Bestand dominant.
- **Dach- und Hallentragwerke:** Dachtragwerk und Fachwerk als besonders materialreiche und oft zugängliche Bauteilquellen.
- **Entwurfsprinzipien:** Design for Disassembly und reversible Fügung als explizit zukunftsorientierte Systemstrategien.
- **Bestandserweiterung:** Aufstockung in Holzbauweise als Strategie, die Bestandserhalt und neue DfD-Schichten kombiniert.

## Querverbindungen zu anderen Kategorien

- **Bauteil:** Systeme setzen sich aus Bauteilen zusammen; die Systemebene erklärt, wie einzelne Bauteile zusammenwirken und ob sie lösbar sind.
- **Verbindung:** Systeme werden durch Verbindungsdetails definiert; reversible Fügung als Systemprinzip setzt konkrete Verbindungstypen voraus.
- **Reuse-Strategie:** Systemwahl bestimmt Strategie; Skelettbau erlaubt Umnutzung und Weiterbauen, während Massivbau häufig in-situ-Erhalt oder Materialrecycling als einzige Optionen lässt.
- **Methode:** DfD als Methode und DfD als Tragwerkssystem-Datei überschneiden sich; `methode/Design_for_Disassembly.md` behandelt die Planungsmethode, diese Kategorie die konstruktiven Systeme.
- **Hürde:** Nicht demontierbare Systeme (Ortbeton, verklebte Schichten) sind eine der wichtigsten strukturellen Hürden für Bauteilwiederverwendung.

---

## Offene Lücken / Ausbaufelder

- **Hybridbau:** Stahl-Holz-Verbund, Holz-Beton-Verbund und andere hybride Systeme fehlen als eigenständige Systemdateien.
- **Modulbau:** Raumzellen- und Modulbauweisen mit hohem DfD-Potenzial sind nicht als eigenständige Systemdatei dokumentiert.
- **Massivholzbau (CLT/BSP-System):** Brettsperrholz-Wandsystem als eigenständige Systemdatei fehlt; derzeit nur in `bauteil/Brettsperrholzdecke.md` und `tragwerkssystem/Holz_Skelettbau.md` gestreift.
- **`to_sort/`-Dateien:** Der Unterordner enthält Entwürfe zu Betonfertigteilen, Ortbeton, Holztragwerk, Träger und Tragende Wände; diese sollten in die Hauptkategorie integriert oder gelöscht werden.
