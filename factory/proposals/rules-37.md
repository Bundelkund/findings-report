# Regel-Vorschlag rules-37 (Factory, F-12)

> Vorschlag, keine Regel. Die Factory aendert factory/RULES.md nie; Florian uebernimmt den Diff von Hand (oder schliesst den PR). Dieser PR wird nie automatisch gemergt.

## Begruendung

Die Ursache-Kategorie spec (Akzeptanzkriterien unklar oder offene Fachfrage) trat in 2 Issues auf (#37, #4). Als Regel stuende sie der Triage und dem Architektur-Loop vor dem ersten Modellaufruf zur Verfuegung;
heute zahlt jedes Issue den Fehler neu, bis es eskaliert.

## Belege (aus factory/knowledge.md auf main)

- #37 (2026-10-24): Akzeptanzkriterien mit unscharfen Formulierungen wie 'Leerer Platzhalter' oder ungedeckten festen Pruefstrings sind nicht pruefbar; Requirement-Deckel von 2 Runden wurde erreicht, Spec braucht
- #4 (2026-10-13): Bei HTML-Berichtsaufgaben mit Kopf, Befund-Liste und CSS blieb eine Fachfrage offen, die das Modell nicht raten darf; der Requirement-Loop stoppt vor dem Dev-Lauf und braucht menschliche Klärung.

## Vorgeschlagener Diff fuer factory/RULES.md

```diff
@@ ## Verbote @@
+- Bekannte Grenze (spec, Belege #37, #4): Akzeptanzkriterien mit unscharfen Formulierungen wie 'Leerer Platzhalter' oder ungedeckten festen Pruefstrings sind nicht pruefbar; Requirement-Deckel von 2 Runden wurde erreicht, Spec braucht
```
