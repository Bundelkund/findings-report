# Testing-Bericht Issue #45

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `3da82d2`
- Tests geschrieben von `anthropic/claude-sonnet-5.5` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 5 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_mit_ort_gueltig | Ausgabe: test_ak1_mit_ort_gueltig ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_ohne_ort_gueltig | Ausgabe: test_ak2_ohne_ort_gueltig ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_ungueltiger_ort | Ausgabe: test_ak3_ungueltiger_ort ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_html_ort | Ausgabe: test_ak4_html_ort ... ok
AK5 | pass | Stufe: 3 | Test: test_ak5_ohne_ort_kein_element | Ausgabe: test_ak5_ohne_ort_kein_element ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Ein Bericht mit drei Befunden, einer davon mit `"ort": "render.py:42"`, ist gueltig: bei der reinen Pruefung (Aufruf mit nur der JSON-Datei, ohne HTML-Datei) meldet das Programm genau `OK: 3 Befunde` (Exit 0).
- AK2: Ein Bericht mit drei Befunden ohne `ort` ist gueltig wie bisher: bei der reinen Pruefung (nur JSON-Datei) meldet das Programm genau `OK: 3 Befunde` (Exit 0).
- AK3: `ort` als Nicht-Text (z.B. die Zahl 42) oder als leerer Text `""` wird abgelehnt: Exit 2 und eine Meldung, die `findings[<i>].ort` nennt (bei einem Befund an erster Stelle: `findings[0].ort`).
- AK4: In der HTML-Seite steht der Ort in der Zeile (`<li>`) des jeweiligen Befunds in genau einem Element mit der Klasse `ort`, nach dem Element mit der Befund-ID, HTML-escaped (`<script>x</script>` als Ort erscheint als `&lt;script&gt;x&lt;/script&gt;`).
- AK5: Die Zeile eines Befunds ohne `ort` enthaelt kein Element mit der Klasse `ort`.
