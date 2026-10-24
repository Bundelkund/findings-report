# Regel-Vorschlag rules-37 (Factory, F-12)

> Vorschlag, keine Regel. Die Factory aendert factory/RULES.md nie; Florian uebernimmt den Diff von Hand (oder schliesst den PR). Dieser PR wird nie automatisch gemergt.

## Begruendung

Die Ursache-Kategorie budget (Budget oder Deckel erreicht) trat in 2 Issues auf (#37, #4). Als Regel stuende sie der Triage und dem Architektur-Loop vor dem ersten Modellaufruf zur Verfuegung;
heute zahlt jedes Issue den Fehler neu, bis es eskaliert.

## Belege (aus factory/knowledge.md auf main)

- #37 (2026-10-24): Das Issue-Budget von 1,00 USD war nach etwa 1,05 USD verbraucht; Dev und Review verursachten dabei den größten Anteil der Kosten.
- #4 (2026-10-13): Das Issue-Budget von 1,0 USD ist im Repo-Ablauf schnell erreicht; Architektur und Anforderungsanalyse verbrauchen den größten Teil, wodurch der Lauf in den Needs-Human-Zustand kippt.

## Vorgeschlagener Diff fuer factory/RULES.md

```diff
@@ ## Verbote @@
+- Bekannte Grenze (budget, Belege #37, #4): Das Issue-Budget von 1,00 USD war nach etwa 1,05 USD verbraucht; Dev und Review verursachten dabei den größten Anteil der Kosten.
```
