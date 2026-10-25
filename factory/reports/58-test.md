# Testing-Bericht Issue #58

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `75df9a4`
- Tests geschrieben von `anthropic/claude-sonnet-5.5` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 3 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_help_stdout_und_exit0 | Ausgabe: test_ak1_help_stdout_und_exit0 ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_help_stderr_leer | Ausgabe: test_ak2_help_stderr_leer ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_ohne_argumente | Ausgabe: test_ak3_ohne_argumente ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: AK1: `python3 -m findings_report --help` gibt auf die Standardausgabe eine Zeile aus, die mit `Verwendung:` beginnt und `<bericht.json>` enthaelt, und endet mit Exit-Code 0.
- AK2: AK2: `python3 -m findings_report --help` schreibt nichts auf die Fehlerausgabe.
- AK3: AK3: `python3 -m findings_report` ohne Argumente endet mit Exit-Code 2 und schreibt auf die Fehlerausgabe genau eine Zeile, die mit `Verwendung:` beginnt und `<bericht.json>` enthaelt.
