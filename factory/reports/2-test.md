# Testing-Bericht Issue #2

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `81ddd72`
- Tests geschrieben von `google/gemini-2.5-flash` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 5 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_valid_report_exit_code_and_output | Ausgabe: test_ak1_valid_report_exit_code_and_output ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_file_not_exists_exit_code_and_message | Ausgabe: test_ak2_file_not_exists_exit_code_and_message ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_invalid_json_exit_code_and_message | Ausgabe: test_ak3_invalid_json_exit_code_and_message ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_missing_title_field, test_ak4_missing_verdict_field, test_ak4_missing_findings_field | Ausgabe: test_ak4_missing_title_field ... ok; test_ak4_missing_verdict_field ... ok; test_ak4_missing_findings_field ... ok
AK5 | pass | Stufe: 3 | Test: test_ak5_invalid_verdict_value, test_ak5_invalid_severity_value | Ausgabe: test_ak5_invalid_verdict_value ... ok; test_ak5_invalid_severity_value ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Gültiger Bericht → Exit-Code 0 und genau eine Ausgabezeile `OK: <Anzahl> Befunde`.
- AK2: Datei existiert nicht → Exit-Code 2 und eine Meldung, die den Dateinamen nennt.
- AK3: Datei ist kein gültiges JSON → Exit-Code 2 und eine Meldung „kein gültiges JSON“.
- AK4: Ein Pflichtfeld fehlt (`title`, `verdict`, `findings`) → Exit-Code 2 und die Meldung nennt den Namen des fehlenden Feldes.
- AK5: `verdict` oder `severity` hat einen unerlaubten Wert → Exit-Code 2 und die Meldung nennt den Wert und die erlaubten Werte.
