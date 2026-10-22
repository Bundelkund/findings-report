# Testing-Bericht Issue #25

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `38d826a`
- Tests geschrieben von `z-ai/glm-5.3` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 6 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_badge_elemente_mit_schweregrad | Ausgabe: test_ak1_badge_elemente_mit_schweregrad ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_badge_vor_titel_im_quelltext | Ausgabe: test_ak2_badge_vor_titel_im_quelltext ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_hintergrundfarben_der_badge_klassen | Ausgabe: test_ak3_hintergrundfarben_der_badge_klassen ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_kontrast_mindestens_45 | Ausgabe: test_ak4_kontrast_mindestens_45 ... ok
AK5 | pass | Stufe: 3 | Test: test_ak5_viewport_und_maximale_breite | Ausgabe: test_ak5_viewport_und_maximale_breite ... ok
AK6 | pass | Stufe: 3 | Test: test_ak6_titel_escaped | Ausgabe: test_ak6_titel_escaped ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Fuer das Canary-JSON aus dem Issue erzeugt python3 -m findings_report <eingabe> <ausgabe> mit Exitcode 0 eine HTML-Datei, in der je Fund ein Element mit Klasse badge und Klasse badge-<schweregrad klein> (z.B. badge-critical) steht, dessen Text genau dem Schweregrad entspricht (CRITICAL, HIGH, MEDIUM, LOW, INFO).
- AK2: Innerhalb jedes Fund-Eintrags steht das Badge im HTML-Quelltext vor dem Titeltext des Fundes.
- AK3: Das eingebettete CSS legt fuer badge-critical eine rote, fuer badge-high eine orange, fuer badge-medium eine gelbe und fuer badge-low und badge-info eine graue Hintergrundfarbe als Hex-Wert fest (rot: Farbton 345-15 Grad, orange: 16-45 Grad, gelb: 46-65 Grad, grau: Saettigung unter 15 Prozent).
- AK4: Fuer jede der fuenf Badge-Klassen hat die im CSS als Hex angegebene Textfarbe zur Hintergrundfarbe ein Kontrastverhaeltnis nach WCAG 2.x von mindestens 4,5:1.
- AK5: Die Seite enthaelt ein meta viewport mit width=device-width, und im CSS kommt keine width- oder min-width-Angabe mit einem px-Wert ueber 390 vor.
- AK6: Ein Fund mit dem Titel <script>alert(1)</script> & "x" erscheint in der Ausgabe escaped (&lt;script&gt;, &amp;), und der rohe String <script>alert(1)</script> kommt nicht vor.
