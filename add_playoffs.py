import json
import os

fixtures_path = 'data/fixtures.json'

with open(fixtures_path, 'r', encoding='utf-8') as f:
    fixtures_data = json.load(f)

fixtures = fixtures_data.get('matches', [])

# Check if playoffs already exist
if any(m['stage'] != 'group' for m in fixtures):
    print("Playoffs already exist.")
else:
    playoffs = []
    
    # 1/16 Финала (16 матчей)
    for i in range(1, 17):
        playoffs.append({
            "id": f"R32-{i}",
            "stage": "round_of_32",
            "datetime_utc": f"2026-06-{28 + (i//4):02d}T18:00:00Z",
            "home": f"Winner Grp {chr(64+(i%12)+1)}",
            "away": f"Runner-up Grp {chr(64+((i+1)%12)+1)}",
            "status": "scheduled",
            "home_score": None,
            "away_score": None,
            "decided_by": None,
            "shootout_winner": None
        })
        
    # 1/8 Финала (8 матчей)
    for i in range(1, 9):
        playoffs.append({
            "id": f"R16-{i}",
            "stage": "round_of_16",
            "datetime_utc": f"2026-07-04T18:00:00Z",
            "home": f"Winner R32-{i*2-1}",
            "away": f"Winner R32-{i*2}",
            "status": "scheduled",
            "home_score": None,
            "away_score": None,
            "decided_by": None,
            "shootout_winner": None
        })

    # 1/4 Финала (4 матча)
    for i in range(1, 5):
        playoffs.append({
            "id": f"QF-{i}",
            "stage": "quarter",
            "datetime_utc": f"2026-07-09T18:00:00Z",
            "home": f"Winner R16-{i*2-1}",
            "away": f"Winner R16-{i*2}",
            "status": "scheduled",
            "home_score": None,
            "away_score": None,
            "decided_by": None,
            "shootout_winner": None
        })

    # 1/2 Финала (2 матча)
    for i in range(1, 3):
        playoffs.append({
            "id": f"SF-{i}",
            "stage": "semi",
            "datetime_utc": f"2026-07-14T18:00:00Z",
            "home": f"Winner QF-{i*2-1}",
            "away": f"Winner QF-{i*2}",
            "status": "scheduled",
            "home_score": None,
            "away_score": None,
            "decided_by": None,
            "shootout_winner": None
        })

    # Матч за 3-е место (1 матч)
    playoffs.append({
        "id": "3RD-1",
        "stage": "third_place",
        "datetime_utc": f"2026-07-18T18:00:00Z",
        "home": "Loser SF-1",
        "away": "Loser SF-2",
        "status": "scheduled",
        "home_score": None,
        "away_score": None,
        "decided_by": None,
        "shootout_winner": None
    })

    # Финал (1 матч)
    playoffs.append({
        "id": "FIN-1",
        "stage": "final",
        "datetime_utc": f"2026-07-19T18:00:00Z",
        "home": "Winner SF-1",
        "away": "Winner SF-2",
        "status": "scheduled",
        "home_score": None,
        "away_score": None,
        "decided_by": None,
        "shootout_winner": None
    })
    
    fixtures.extend(playoffs)
    fixtures_data['matches'] = fixtures
    with open(fixtures_path, 'w', encoding='utf-8') as f:
        json.dump(fixtures_data, f, ensure_ascii=False, indent=2)
    print("Added 32 playoff matches to fixtures.json")
