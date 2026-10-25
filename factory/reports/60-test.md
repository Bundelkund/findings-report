# Testing-Bericht Issue #60

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `689298e`
- Tests geschrieben von `anthropic/claude-sonnet-5.5` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 3 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_data_id_simple | Ausgabe: test_ak1_data_id_simple ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_data_id_escaped | Ausgabe: test_ak2_data_id_escaped ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_no_findings_no_data_id | Ausgabe: test_ak3_no_findings_no_data_id ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Ein Bericht mit einem Befund der ID `F1` erzeugt ein `li`, dessen Start-Tag das Attribut `data-id="F1"` enthaelt.
- AK2: Ein Befund mit der ID `a"b<c` erscheint als `data-id="a&quot;b&lt;c"`, nie als rohes `a"b<c` im Attribut.
- AK3: Die HTML-Ausgabe eines Berichts ohne Befunde enthaelt den String 'data-id' nicht.
