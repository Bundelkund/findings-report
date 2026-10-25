# Testing-Bericht Issue #67

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `1692bd1`
- Tests geschrieben von `anthropic/claude-sonnet-5.5` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 4 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_natural_numbers | Ausgabe: test_ak1_natural_numbers ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_case_insensitive | Ausgabe: test_ak2_case_insensitive ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_ids_without_digits_last | Ausgabe: test_ak3_ids_without_digits_last ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_severity_still_first | Ausgabe: test_ak4_severity_still_first ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Drei Befunde mit Schweregrad HIGH und den IDs `F10`, `F2`, `F1` erscheinen in der Seite in der Reihenfolge `F1`, `F2`, `F10`.
- AK2: Ein Befund `f1` und ein Befund `F2` (beide MEDIUM, in der Eingabe in der Reihenfolge `F2`, `f1`) erscheinen als `f1`, `F2`.
- AK3: Ein Befund mit der ID `zeta` und einer mit der ID `Alpha` (beide LOW) stehen hinter einem LOW-Befund mit der ID `F3` und untereinander als `Alpha`, `zeta`.
- AK4: Ein CRITICAL-Befund mit der ID `F99` steht weiterhin vor einem HIGH-Befund mit der ID `F1`.
