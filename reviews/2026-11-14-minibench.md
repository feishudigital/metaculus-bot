# Review 2026-11-14: questions resolved in the last 30 days

Data: `review_bot.yaml` run 43604852975 (scores), run 43605302759 (report sections of the five
worst numeric/discrete questions). Scores are spot peer scores.

## Summary
- MiniBench round 2026-11-02: 32 scored, sum +114.8, mean +3.6, 20 of 32 positive.
  Main tournament: 1 resolved (46284, +7.3).
- Binary questions carry the score: 12 questions, mean +16.2, 10 positive.
- Numeric (8, mean -2.1) and discrete (11, mean -7.0) questions lose it.
- Every question was scored about 2-3 h after the bot forecast, so late updating by other
  forecasters does not explain the losses (tested across all 33).

## Calibration check (all 19 numeric/discrete questions with a trace)
Resolution below the bot's 10th or above its 90th percentile: 3 of 19 (expected about 4).
The distributions are not systematically too narrow. The losses come from where the centre sat
on individual questions, and from peers being sharper on small integer counts.

## Worst five
- [46406](https://www.metaculus.com/questions/46406/) EIA crude inventory change, -87.3.
  Resolved +4660; median about -1000, P90 about 4000. Research was complete (recent prints,
  seasonality, SPR release, refinery maintenance). Forecasters noted that early November
  usually brings builds, then still leaned on the four-week draw streak. Forecast ten days ahead
  of a noisy weekly figure: mostly variance, with a slight trend-following tilt.
- [46424](https://www.metaculus.com/questions/46424/) USDA loose white Large eggs, -50.6.
  Resolved 73 cents; median about 38, P90 61-66. Research had the right numbers. All three
  forecasters named the upside scenario themselves ("60 to 90 cents", HPAI plus Thanksgiving,
  37 to 74 cents jump in March) and gave it only about 10%.
- [46413](https://www.metaculus.com/questions/46413/) InfoGripe capitals, -21.5.
  Resolved 4; median 4-5. Centre right, peers sharper. No process failure found.
- [46419](https://www.metaculus.com/questions/46419/) Fifth Circuit announcements, -17.8.
  Resolved 1; final forecast 49.6% on 0, 20% on 1. No mass below zero (checked in the
  summary section). Reasonable, unlucky.
- [46421](https://www.metaculus.com/questions/46421/) IEA Venezuela supply, -16.4.
  Resolved 1.14 (down); median 1.16-1.18, leaning up on a Polymarket market. Outcome at P10.

## Patterns
- No research gaps in any of the five: the deciding facts or scenarios were in the research.
- Two of five (46406, 46424) anchored on the latest print plus recent trend while the bot's
  own reasoning pointed at a seasonal move the other way or a fat upper tail.

## Suggestions
- No code change yet. One round, 19 numeric/discrete questions; the evidence for a prompt
  change rests on two questions. Re-check once the main tournament has 20+ resolved numeric
  questions: if the resolution keeps landing in the tail the forecasters named themselves,
  add a prompt line to weigh a named seasonal or tail scenario in the percentiles instead of
  anchoring on the last print (would have helped 46406, 46424).
