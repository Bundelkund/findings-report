# Regel-Vorschlag rules-37 (Factory, F-12)

> Vorschlag, keine Regel. Die Factory aendert factory/RULES.md nie; Florian uebernimmt den Diff von Hand (oder schliesst den PR). Dieser PR wird nie automatisch gemergt.

## Begruendung

Die Ursache-Kategorie test (Tests oder Pruefer scheiterten) trat in 2 Issues auf (#37, #2). Als Regel stuende sie der Triage und dem Architektur-Loop vor dem ersten Modellaufruf zur Verfuegung;
heute zahlt jedes Issue den Fehler neu, bis es eskaliert.

## Belege (aus factory/knowledge.md auf main)

- #37 (2026-10-24): Das optionale Feld 'ort' im Eingabeformat laesst bestehende Tests zur Zusammenfassung und Schweregrad-Zaehlung rot werden; diese Regression blieb auch nach mehreren Neuentwuerfen bestehen.
- #2 (2026-10-13): Die von der Testphase selbst geschriebenen Tests scheiterten in vier Versuchen an der eigenen Referenz (AK5 durchgehend rot); der Testing-Loop eskalierte ohne brauchbare Tests.

## Vorgeschlagener Diff fuer factory/RULES.md

```diff
@@ ## Verbote @@
+- Bekannte Grenze (test, Belege #37, #2): Das optionale Feld 'ort' im Eingabeformat laesst bestehende Tests zur Zusammenfassung und Schweregrad-Zaehlung rot werden; diese Regression blieb auch nach mehreren Neuentwuerfen bestehen.
```
