# Testing-Bericht Issue #2

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `11423e2`
- Tests geschrieben von `qwen/qwen3-coder-next` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 5 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_valid_report | Ausgabe: test_ak1_valid_report ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_file_not_found | Ausgabe: test_ak2_file_not_found ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_invalid_json | Ausgabe: test_ak3_invalid_json ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_missing_title, test_ak4_missing_verdict, test_ak4_missing_findings | Ausgabe: test_ak4_missing_title ... ok; test_ak4_missing_verdict ... ok; test_ak4_missing_findings ... ok
AK5 | pass | Stufe: 3 | Test: test_ak5_invalid_verdict, test_ak5_invalid_severity | Ausgabe: test_ak5_invalid_verdict ... ok; test_ak5_invalid_severity ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Gültiger Bericht → Exit-Code 0 und genau eine Ausgabezeile `OK: <Anzahl> Befunde`.
- AK2: Datei existiert nicht → Exit-Code 2 und eine Meldung, die den Dateinamen nennt.
- AK3: Datei ist kein gültiges JSON → Exit-Code 2 und eine Meldung „kein gültiges JSON“.
- AK4: Ein Pflichtfeld fehlt (`title`, `verdict`, `findings`) → Exit-Code 2 und die Meldung nennt den Namen des fehlenden Feldes.
- AK5: `verdict` oder `severity` hat einen unerlaubten Wert → Exit-Code 2 und die Meldung nennt den Wert und die erlaubten Werte.
