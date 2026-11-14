# STATE — Metaculus-Prognose-Bot

**Stand:** 2026-11-14 · Prüfung: läuft sauber; forecasting-tools 0.3.5 → 0.3.7

## Was es ist
Fork von `Metaculus/metac-bot-template` als `feishudigital/metaculus-bot` (öffentlich).
Läuft per GitHub Actions im FutureEval-Bot-Wettbewerb (Herbst 2026) und in der MiniBench.
Hintergrund, Regeln, Preisgeld: Memory `reference-passiv-ki-trading-optionen-2026-10`.

## Aufbau
- Recherche: Claude Sonnet 5.5 mit Websuche (max. 5 Suchen je Frage, über litellm `web_search_options`).
- Prognose: Opus 5.5 im Hauptwettbewerb und in der MiniBench (Kevin 14.11.), Median. Tempo-Regel (Kevin 14.11.:
  „immer den vollen Betrag ausnutzen“): unter gleichmäßigem Monatstempo (95 $ × Monatsanteil) 2 Recherchen × 5 Prognosen
  Effort high (~0,60 $/Frage), sonst 1 × 3 medium (~0,20 $) (`budget.thorough_allowed`). Sonnet/MiniBench aus erst, wenn 2 $ × Resttage nicht mehr passen.
- Parser/Zusammenfassung: Claude Haiku 5.5.
- Kostendeckel `budget.py`: Kostenbuch `kosten.json` (je Monat, vom Workflow zurück-committet).
  Kevin 28.10.: Der Bot darf das ganze freie API-Guthaben nutzen (100 $/Monat, Reset am 1.), aber NIE darüber. Kein anderes Projekt nutzt die API zurzeit; ändert sich das, sagt Kevin Bescheid → Deckel senken.
  Deckel = Repo-Variable `BOT_MONTHLY_BUDGET_USD` (ohne Variable 95 $, Kevin 02.11.; 5 $ Reserve für Zählfehler);
  `BOT_BUDGET_MONTH_OVERRIDE` = „JJJJ-MM=Betrag“ nur für einen Monat. Am Deckel Pause bis Monatsende.
- Nur die Prognose-Jobs (Tournament + Test) teilen die Warteschlange `bot-forecast` (max. 180 min; seit 02.11., weil am
  30.10. ein hängender save_ledger 24 h alles blockierte → 4 Fragen verpasst). Der Bot-Job hat nur Leserechte und
  checkt immer die Spitze von main aus. Er übergibt nur die eigenen Laufkosten (`run_cost.json`) als Artefakt an
  `save_ledger` (einziger Job mit Schreibrecht); der addiert sie auf `kosten.json` an der Spitze von main
  (`python3 budget.py merge-run-cost`, bis zu 3 Versuche). So überschreibt kein veralteter Stand neuere Summen.

## Offen
1. ✓ Secrets `METACULUS_TOKEN` + `ANTHROPIC_API_KEY`; Cup-Workflow aus (kein Bot-Preisgeld); Test nur von Hand.
2. Auslöser: Pi-Cron `3,33` (Dispatch-API, Kevins OK 02.11.), GitHub-Cron nur `47 */3` als Rückfall.
   Prüfung 14.11.: 279/281 Läufe 08.–14.11. grün (2 Ausreißer 11.11. ohne Kosten), Pi-Fehler nur 3× 04./05.11. Haupt: 40/40
   neuesten beantwortet. Ergebnis 14.11. (`reviews/2026-11-14-minibench.md`): MiniBench 32 Fragen Schnitt +3,6
   (Ja/Nein +16,2, Zahlen −2,1, Stufen −7,0; keine Recherchelücke, kein Code-Fix); neu prüfen ab 20 Zahlenfragen Haupt.
3. **forecasting-tools 0.3.5 zählte jeden LLM-Aufruf doppelt** (Mock-Test 14.11.: 2,2e-5 vs. litellm 1,1e-5; 0.3.7 korrekt).
   Kostenbuch halbiert (f49824f): Okt 3,03 $, Nov 21,65 $ = Console 21,36 $ (Schlüssel „Metaculus“, 14.11.).
   Gemessen 14.11.: normal ~0,20 $/Frage, gründlich (2×5, high) 0,57 $/Frage; zwei Testläufe (bot-testing-area) 8,23 $,
   Testläufe seither auf 5 $ gedeckelt. Gap-Science-Schlüssel: Kevin deaktiviert ihn in der Console.

## Fallen
- forecasting-tools 0.3.5 lässt `temperature` automatisch weg, wenn ein Modell ihn ablehnt; trotzdem nie setzen.
- Gratis-Guthaben von Metaculus: Herbst geschlossen, neuer Antrag wenige Wochen vor Januar.
- Fork: Zeitplan erst nach Klick „I understand my workflows…“ + Push auf main; zu viele Läufe → GitHub sperrt den Fork.
