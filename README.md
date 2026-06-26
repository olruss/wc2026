# World Cup 2026 — Prediction Pool (2 players)

A tiny, local, no-dependency system for tracking head-to-head World Cup
predictions. Data lives in plain JSON; `compute.py` calculates standings.

## Scoring (per match)

Prediction `A–B` vs. actual result:

| Component  | Points | Condition                                  |
|------------|:------:|--------------------------------------------|
| Outcome    | **3**  | Correct win / draw / loss                  |
| Home goals | **1**  | Home team's exact goal count               |
| Away goals | **1**  | Away team's exact goal count               |
| Margin     | **1**  | Signed goal difference correct             |
| Exact score| **6**  | all of the above stack                     |

**Penalties (knockouts):** the scored result = regulation/ET score **+1 to the
shootout winner**. E.g. 1–1 then home wins on pens → scored as **2–1**.

## Favorite teams

Each player picks **3 teams** (locked before the tournament). A team earns points
for the **furthest stage it reaches** (not cumulative):

| Stage         | Points |
|---------------|:------:|
| Round of 32   | 2 *(tunable; new 48-team format)* |
| Round of 16   | 3      |
| Quarter-final | 6      |
| Semi-final    | 12     |
| Final reached | 20     |
| Champion      | 30     |

Both players may pick the same team.

## Tie-breakers (overall standings)

total points → most exact scores → most correct outcomes.

## Files

```
config.json            scoring + favorite tiers + tie-breakers (edit to tune)
data/fixtures.json     all matches: schedule, results, penalty info
data/predictions.json  each player's predicted scores, keyed by match id
data/favorites.json    each player's 3 favorite teams
compute.py             prints standings + breakdown + favorite points
```

## Workflow

1. Before a round, look up the upcoming match ids in `data/fixtures.json`.
2. Hand your predictions to Claude (or edit `predictions.json` directly), e.g.
   `"oleg: A3 2-1, A4 1-1; friend: A3 0-0, A4 2-0"`.
3. As matches finish, results get filled into `fixtures.json`.
4. Run `python3 compute.py` to see the current table.

## Run

```
python3 compute.py
```
