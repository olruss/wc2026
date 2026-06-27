#!/usr/bin/env python3
"""World Cup 2026 prediction pool — scoring & standings.

Reads config.json + data/{fixtures,predictions,favorites}.json and prints
the current standings, a per-match breakdown, and favorite-team points.

No third-party dependencies. Run:  python3 compute.py
"""
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

# Stage ordering for "furthest stage reached" by a favorite team.
# third_place sits level with semi (those teams lost in the semis).
STAGE_RANK = {
    "group": 0,
    "round_of_32": 1,
    "round_of_16": 2,
    "quarter": 3,
    "semi": 4,
    "third_place": 4,
    "final": 5,
}
# Maps a furthest-reached stage to the favorites config key.
STAGE_TO_FAV_KEY = {
    "round_of_32": "round_of_32",
    "round_of_16": "round_of_16",
    "quarter": "quarter",
    "semi": "semi",
    "final": "final",
}


def load(name):
    with open(DATA / name if not name.endswith("config.json") else ROOT / name) as f:
        return json.load(f)


def sign(x):
    return (x > 0) - (x < 0)


def effective_result(m):
    """Actual (home, away) used for scoring, applying the penalty rule:
    +1 goal to the shootout winner."""
    h, a = m["home_score"], m["away_score"]
    if m.get("decided_by") == "penalties":
        if m.get("shootout_winner") == m["home"]:
            h += 1
        else:
            a += 1
    return h, a


def score_prediction(pred, act, scoring):
    ph, pa = pred
    ah, aa = act
    pts = 0
    detail = []
    if sign(ph - pa) == sign(ah - aa):
        pts += scoring["outcome"]; detail.append("O")
    if ph == ah:
        pts += scoring["home_goals"]; detail.append("H")
    if pa == aa:
        pts += scoring["away_goals"]; detail.append("A")
    if (ph - pa) == (ah - aa):
        pts += scoring["margin"]; detail.append("M")
    return pts, "".join(detail)


def team_furthest_stage(matches):
    """Furthest stage each team appears in (only real teams, not placeholders),
    plus the champion (winner of a finished final)."""
    furthest = {}
    champion = None
    for m in matches:
        rank = STAGE_RANK.get(m["stage"], 0)
        for team in (m["home"], m["away"]):
            if not team or team.lower().startswith(("winner", "runner", "loser", "1st", "2nd", "3rd", "best")):
                continue
            if team not in furthest or rank > STAGE_RANK.get(furthest[team], 0):
                furthest[team] = m["stage"]
        if m["stage"] == "final" and m["status"] == "finished":
            ah, aa = effective_result(m)
            champion = m["home"] if ah > aa else m["away"]
    return furthest, champion


def favorite_points(team, furthest, champion, fav_cfg):
    if team == champion:
        return fav_cfg["champion"], "champion"
    stage = furthest.get(team)
    if stage is None:
        return 0, "not in bracket yet"
    key = STAGE_TO_FAV_KEY.get(stage)
    if key is None:  # still in group stage
        return 0, "group stage"
    return fav_cfg[key], stage


def calculate_groups(matches):
    groups = {}
    for m in matches:
        if m["stage"] != "group":
            continue
        g = m["group"]
        if g not in groups:
            groups[g] = {}
        for team in (m["home"], m["away"]):
            if team not in groups[g]:
                groups[g][team] = {"team": team, "pld": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0, "gd": 0, "pts": 0}
        
        if m["status"] == "finished":
            h, a = effective_result(m)
            home, away = m["home"], m["away"]
            
            groups[g][home]["pld"] += 1
            groups[g][away]["pld"] += 1
            groups[g][home]["gf"] += h
            groups[g][away]["gf"] += a
            groups[g][home]["ga"] += a
            groups[g][away]["ga"] += h
            groups[g][home]["gd"] += (h - a)
            groups[g][away]["gd"] += (a - h)
            
            if h > a:
                groups[g][home]["w"] += 1
                groups[g][home]["pts"] += 3
                groups[g][away]["l"] += 1
            elif h < a:
                groups[g][away]["w"] += 1
                groups[g][away]["pts"] += 3
                groups[g][home]["l"] += 1
            else:
                groups[g][home]["d"] += 1
                groups[g][home]["pts"] += 1
                groups[g][away]["d"] += 1
                groups[g][away]["pts"] += 1

    # Convert to sorted lists
    sorted_groups = {}
    for g, teams in sorted(groups.items()):
        # Sort by Pts, then GD, then GF
        sorted_teams = sorted(teams.values(), key=lambda x: (x["pts"], x["gd"], x["gf"]), reverse=True)
        sorted_groups[g] = sorted_teams
    return sorted_groups


def extract_playoffs(matches):
    playoffs = {}
    for m in matches:
        if m["stage"] == "group":
            continue
        s = m["stage"]
        if s not in playoffs:
            playoffs[s] = []
        
        h_score, a_score = ("-", "-")
        if m["status"] == "finished":
            h_score, a_score = effective_result(m)
            
        playoffs[s].append({
            "id": m["id"],
            "home": m["home"],
            "away": m["away"],
            "home_score": h_score,
            "away_score": a_score,
            "status": m["status"]
        })
    return playoffs



def main():
    config = load("config.json")
    fixtures = load("fixtures.json")
    predictions = load("predictions.json")
    favorites = load("favorites.json")
    
    upcoming_ai = {}
    try:
        upcoming_ai = load("upcoming_ai.json")
    except:
        pass

    players = config["players"]
    scoring = config["scoring"]
    fav_cfg = config["favorites"]
    matches = {m["id"]: m for m in fixtures["matches"]}
    finished = [m for m in fixtures["matches"] if m["status"] == "finished"]

    # ---- Match scoring ----
    totals = {p: 0 for p in players}
    exact = {p: 0 for p in players}
    outcomes = {p: 0 for p in players}
    catches = {p: 0 for p in players}
    rows = []  # per match with predictions

    # Matches that either finished or have predictions
    matches_to_score = [m for m in fixtures["matches"] if m["status"] == "finished" or any(predictions.get(p, {}).get(m["id"]) for p in players)]

    for m in sorted(matches_to_score, key=lambda x: x.get("datetime_utc") or ""):
        if not any(predictions.get(p, {}).get(m["id"]) for p in players):
            continue  # nobody bet on this match — skip it
        act = effective_result(m) if m["status"] == "finished" else ("-", "-")
        line = {"id": m["id"], "match": f'{m["home"]} {act[0]}-{act[1]} {m["away"]}',
                "stage": m["stage"], "status": m["status"]}
        for p in players:
            pred = predictions.get(p, {}).get(m["id"])
            if pred is None:
                line[p] = ("--", 0)
                continue
            if m["status"] == "finished":
                pts, detail = score_prediction(pred, act, scoring)
                totals[p] += pts
                if pts == sum(scoring.values()):
                    exact[p] += 1
                elif "O" in detail:
                    outcomes[p] += 1
                elif pts > 0:
                    catches[p] += 1
            else:
                pts = 0
            line[p] = (f'{pred[0]}-{pred[1]}', pts)
            line[f"{p}_pts"] = pts
        rows.append(line)

    # ---- Favorite points ----
    furthest, champion = team_furthest_stage(fixtures["matches"])
    fav_breakdown = {p: [] for p in players}
    for p in players:
        for team in favorites.get(p, []):
            pts, why = favorite_points(team, furthest, champion, fav_cfg)
            totals[p] += pts
            fav_breakdown[p].append((team, pts, why))

    # ---- Output ----
    W = 60
    print("=" * W)
    print(" WORLD CUP 2026 — STANDINGS".center(W))
    print("=" * W)

    ranked = sorted(players, key=lambda p: (totals[p], exact[p], outcomes[p]), reverse=True)
    for i, p in enumerate(ranked, 1):
        lead = "  " if i > 1 else "* "
        print(f"{lead}{i}. {p:<12} {totals[p]:>4} pts   "
              f"(exact: {exact[p]}, outcomes: {outcomes[p]}, catches: {catches[p]})")
    print()

    if rows:
        print("-" * W)
        print(" MATCH BREAKDOWN  (legend: O=outcome H=home A=away M=margin)")
        print("-" * W)
        for r in rows:
            status_tag = "" if r["status"] == "finished" else " (pending)"
            print(f' {r["id"]:<6} {r["match"]}{status_tag}')
            for p in players:
                pred, pts = r[p]
                pts_str = str(pts) if r["status"] == "finished" else "?"
                print(f'        {p:<10} {pred:>6}  -> {pts_str} pts')
        print()

    print("-" * W)
    print(" FAVORITE TEAMS")
    print("-" * W)
    for p in players:
        favs = fav_breakdown[p]
        if not favs:
            print(f' {p}: (none picked yet)')
            continue
        sub = sum(pts for _, pts, _ in favs)
        print(f' {p}: {sub} pts')
        for team, pts, why in favs:
            print(f'      {team:<18} {pts:>3}  ({why})')
    if champion:
        print(f'\n Champion: {champion}')
    print("=" * W)

    # ---- Export to docs/data.js for Web Dashboard ----
    DOCS.mkdir(exist_ok=True)
    
    history = []
    matchDetails = []
    for r in rows:
        if r["status"] == "finished":
            history.append({
                "matchId": r["id"],
                "Oleg": r.get("Oleg_pts", 0),
                "Alex": r.get("Alex_pts", 0)
            })
        matchDetails.append({
            "id": r["id"],
            "match": r["match"],
            "stage": r["stage"],
            "status": r["status"],
            "Oleg_pred": r.get("Oleg", ("--", 0))[0],
            "Oleg_pts": r.get("Oleg_pts", 0),
            "Alex_pred": r.get("Alex", ("--", 0))[0],
            "Alex_pts": r.get("Alex_pts", 0)
        })
        
    # Add favorite points as a final history item
    history.append({
        "matchId": "Favorites",
        "Oleg": sum(pts for _, pts, _ in fav_breakdown.get("Oleg", [])),
        "Alex": sum(pts for _, pts, _ in fav_breakdown.get("Alex", []))
    })
    
    group_standings = calculate_groups(fixtures["matches"])
    playoff_bracket = extract_playoffs(fixtures["matches"])
    
    from datetime import datetime
    # Filter scheduled matches
    scheduled = [m for m in fixtures["matches"] if m["status"] == "scheduled"]
    
    data_json = {
        "currentScores": {
            p: totals[p] for p in players
        },
        "stats": {
            p: {"exact": exact[p], "outcomes": outcomes[p], "catches": catches[p]} for p in players
        },
        "favorites_breakdown": {
            p: [{"team": team, "pts": pts, "why": why} for team, pts, why in fav_breakdown[p]] for p in players
        },
        "history": history,
        "matchDetails": matchDetails,
        "groups": calculate_groups(fixtures["matches"]),
        "playoffs": extract_playoffs(fixtures["matches"]),
        "upcoming": scheduled,
        "upcoming_ai": upcoming_ai,
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    with open(DOCS / "data.js", "w", encoding="utf-8") as f:
        f.write("window.DASHBOARD_DATA = ")
        json.dump(data_json, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"\n[INFO] Web dashboard data exported to {DOCS / 'data.js'}")

    # ---- Cache Busting ----
    # Обновляем версию файлов в index.html, чтобы сбросить кэш у пользователей
    import time
    version = str(int(time.time()))
    index_path = DOCS / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Обновляем CSS
        html = re.sub(r'href="style\.css(\?v=\d+)?"', f'href="style.css?v={version}"', html)
        # Обновляем data.js
        html = re.sub(r'src="data\.js(\?v=\d+)?"', f'src="data.js?v={version}"', html)
        # Обновляем app.js
        html = re.sub(r'src="app\.js(\?v=\d+)?"', f'src="app.js?v={version}"', html)
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[INFO] Cache busted in index.html (version {version})")





if __name__ == "__main__":
    main()
