# Testing-Bericht Issue #35

- Urteil: **pass** · Dev-Runde 2 · Dev-Stand `1f7dfac`
- Tests geschrieben von `z-ai/glm-5.3` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 5 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_alle_fuenf_schweregrade | Ausgabe: test_ak1_alle_fuenf_schweregrade ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_ohne_funde_weglassen | Ausgabe: test_ak2_ohne_funde_weglassen ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_keine_funde | Ausgabe: test_ak3_keine_funde ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_390px_breite | Ausgabe: test_ak4_390px_breite ... ok
AK5 | pass | Stufe: 3 | Test: test_ak5_befehl_bsp_eingabe | Ausgabe: test_ak5_befehl_bsp_eingabe ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Direkt unter dem Titel steht eine Zeile mit der Anzahl je Schweregrad, in der Reihenfolge CRITICAL, HIGH, MEDIUM, LOW, INFO.
- AK2: Schweregrade ohne Funde erscheinen nicht in der Zeile.
- AK3: Ohne jeden Fund steht dort "keine Funde".
- AK4: Die Seite bleibt bei 390 px Breite ohne waagerechtes Scrollen.
- AK5: Der Befehl python3 -m findings_report <eingabe.json> <ausgabe.html> laeuft mit der Beispiel-Eingabe aus dem Issue fehlerfrei und schreibt die Ausgabedatei.
