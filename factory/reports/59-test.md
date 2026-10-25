# Testing-Bericht Issue #59

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `f0d94cd`
- Tests geschrieben von `anthropic/claude-sonnet-5.5` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 3 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_warnung_bei_201_zeichen | Ausgabe: test_ak1_warnung_bei_201_zeichen ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_keine_warnung_bei_200_zeichen | Ausgabe: test_ak2_keine_warnung_bei_200_zeichen ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_html_mit_warnung | Ausgabe: test_ak3_html_mit_warnung ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Ein Bericht mit einem Titel aus 201 Zeichen, aufgerufen mit `python3 -m findings_report bericht.json`, schreibt auf die Fehlerausgabe genau die Zeile `Warnung: Titel hat mehr als 200 Zeichen` und endet mit Exit-Code 0.
- AK2: Ein Bericht mit einem Titel aus genau 200 Zeichen schreibt nichts auf die Fehlerausgabe.
- AK3: Mit zwei Dateien (`bericht.json ausgabe.html`) steht bei einem Titel aus 201 Zeichen dieselbe Warnung auf der Fehlerausgabe, die HTML-Datei wird trotzdem geschrieben und der Titel steht ungekuerzt darin.
