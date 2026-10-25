# Testing-Bericht Issue #66

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `debf199`
- Tests geschrieben von `anthropic/claude-sonnet-5.5` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 4 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_https_link_escaped | Ausgabe: test_ak1_https_link_escaped ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_javascript_plain_text | Ausgabe: test_ak2_javascript_plain_text ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_quotes_escaped | Ausgabe: test_ak3_quotes_escaped ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_plain_path | Ausgabe: test_ak4_plain_path ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Ein Befund mit dem `ort` `https://example.org/a?x=1&y=2` erscheint als `<a href="https://example.org/a?x=1&amp;y=2">` mit demselben (escapten) Text als Linkinhalt.
- AK2: Ein Befund mit dem `ort` `javascript:alert(1)` erscheint nur als einfacher, escapter Text: die Ausgabe enthaelt den Text `javascript:alert(1)`, aber weder `<a href="javascript:alert(1)"` noch `>javascript:alert(1)</a>`.
- AK3: Ein Befund mit dem `ort` `https://example.org/"onmouseover="alert(1)` erzeugt keinen zusaetzlichen Attributnamen: im Start-Tag steht `&quot;`, nie ein rohes `"` mitten im href-Wert.
- AK4: Ein Befund mit dem `ort` `src/app.py:12` erscheint als einfacher, escapter Text ohne Link: die Ausgabe enthaelt `src/app.py:12`, aber weder `<a href="src/app.py:12"` noch `>src/app.py:12</a>`.
