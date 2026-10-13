# Regel-Vorschlag rules-4 (Factory, F-12)

> Vorschlag, keine Regel. Die Factory aendert factory/RULES.md nie; Florian uebernimmt den Diff von Hand (oder schliesst den PR). Dieser PR wird nie automatisch gemergt.

## Begruendung

Die Ursache-Kategorie modell-antwort (Modellantwort verletzt Schema, Laenge oder JSON) trat in 2 Issues auf (#4, #2). Als Regel stuende sie der Triage und dem Architektur-Loop vor dem ersten Modellaufruf zur Verfuegung;
heute zahlt jedes Issue den Fehler neu, bis es eskaliert.

## Belege (aus factory/knowledge.md auf main)

- #4 (2026-10-13): Die Architektur-Antwort des Modells scheiterte zweimal am Schema, weil das Feld dateien.1.aenderung die erlaubte Laenge von 400 Zeichen ueberschritt; Beschreibungen fuer Aenderungen muessen knapp
- #2 (2026-10-13): Der Testing-Pruefer (google/gemini-3.6-flash) lieferte bei der Spec-Pruefung wiederholt HTTP 400 vom Modellaufruf, daher kein gueltiges Urteil ueber die Spec; das Issue blieb bei needs-human.

## Vorgeschlagener Diff fuer factory/RULES.md

```diff
@@ ## Verbote @@
+- Bekannte Grenze (modell-antwort, Belege #4, #2): Die Architektur-Antwort des Modells scheiterte zweimal am Schema, weil das Feld dateien.1.aenderung die erlaubte Laenge von 400 Zeichen ueberschritt; Beschreibungen fuer Aenderungen muessen knapp
```
