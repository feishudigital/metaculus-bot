# STATE — Metaculus-Prognose-Bot

**Stand:** 2026-10-28 · Bot vorbereitet, noch nicht live

## Was es ist
Fork von `Metaculus/metac-bot-template` als `feishudigital/metaculus-bot` (öffentlich).
Läuft per GitHub Actions im FutureEval-Bot-Wettbewerb (Herbst 2026) und in der MiniBench.
Hintergrund, Regeln, Preisgeld: Memory `reference-passiv-ki-trading-optionen-2026-10`.

## Aufbau (Commit c7b73bb)
- Recherche: Claude Sonnet 5.5 mit Websuche (max. 5 Suchen je Frage, über litellm `web_search_options`).
- Prognose: 3× Claude Opus 5.5 (Effort medium), veröffentlicht wird der Median.
- Parser/Zusammenfassung: Claude Haiku 5.5.
- Kostendeckel `budget.py`: Kostenbuch `kosten.json` (je Monat, vom Workflow zurück-committet).
  Kevin 28.10.: Der Bot darf das ganze freie API-Guthaben nutzen (100 $/Monat, Reset am 1.), aber NIE darüber.
  Kein anderes Projekt nutzt die API zurzeit; ändert sich das, sagt Kevin Bescheid → Deckel senken.
  Deckel = Repo-Variable `BOT_MONTHLY_BUDGET_USD` (ohne Variable 85 $, 15 $ Reserve für Zählfehler);
  `BOT_BUDGET_MONTH_OVERRIDE` = „JJJJ-MM=Betrag“ gilt nur für diesen einen Monat. Ab 80 % Sonnet statt Opus,
  am Deckel setzt der Bot bis Monatsende aus. Das Kostenbuch kennt nur die Bot-Kosten.
- Workflows Tournament + Test teilen die Warteschlange `bot-cost-ledger`. Der Bot-Job hat nur Leserechte und
  checkt immer die Spitze von main aus. Er übergibt nur die eigenen Laufkosten (`run_cost.json`) als Artefakt an
  `save_ledger` (einziger Job mit Schreibrecht); der addiert sie auf `kosten.json` an der Spitze von main
  (`python3 budget.py merge-run-cost`, bis zu 3 Versuche). So überschreibt kein veralteter Stand neuere Summen.

## Offen
1. ✓ 28.10.: gh-Scope `workflow` ergänzt, alles auf GitHub.
2. ✓ 28.10.: Workflows Tournament und Metaculus Cup per `gh workflow disable` gesperrt (Cup zahlt Bots kein
   Preisgeld). Aktiv sind nur „Test Bot“ (nur von Hand) und „review_bot“ (wöchentlich, nur lesend).
3. Kevin: Secrets `METACULUS_TOKEN` + `ANTHROPIC_API_KEY` im Repo anlegen.
4. Test Bot (bot-testing-area) laufen lassen: echte Kosten je Frage messen, alle Fragetypen prüfen.
5. Erst danach Tournament-Workflow aktivieren. Nur die ERSTE MiniBench zählt für Leistungsgutschriften.
6. Oktober: 14,49 $ Restguthaben (Kevin 28.10.) → `BOT_BUDGET_MONTH_OVERRIDE=2026-10=12`; ab 01.11. gilt
   automatisch 85 $. Nach dem Testlauf Kostenbuch mit Kevins Restguthaben in der Console vergleichen; zählt der
   Bot genau, Standard-Deckel auf ~92 $ anheben.

## Fallen
- forecasting-tools 0.3.5 lässt `temperature` automatisch weg, wenn ein Modell ihn ablehnt; trotzdem nie setzen.
- litellm 1.105.1 kennt die Preise der 5.5-Modelle und zählt Websuche mit 0,01 $ je Suche.
- Gratis-LLM-Guthaben von Metaculus ist für die Herbstsaison geschlossen; neuer Antrag ein paar Wochen vor Januar.
