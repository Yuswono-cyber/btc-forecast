# btc-cent-forecast-01 entry — consistency-scaled median lean

`main.py` (Python 3.13, standard library only) reads each case (72 hours of
1-minute BTC closes) and writes one guess for the close 240 minutes later.

The house baseline is persistence: guess the checkpoint close. On a broad
local sample that is almost unbeatable — every drift-chasing variant tested
lost to it — and a tie with it pays nothing. This entry therefore starts from
the close and leans only as far as the case's own history agrees with itself:
it adds the median 240-minute change of the given 72 hours, scaled by the
share of those changes that share the median's sign (mapped 50%→0, 100%→1).
In a two-sided tape the lean vanishes; in a one-sided tape it is full.

Local checks: 47,468 cents MAE across 96 synthetic checkpoints cut from the
kit's practice recording (persistence: 47,382 — a wash), and 46,940 vs
persistence's 47,055 on the five practice cases with real futures.
