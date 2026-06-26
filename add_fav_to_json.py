import re

with open('compute.py', 'r', encoding='utf-8') as f:
    compute_code = f.read()

# Replace the "stats" dictionary addition to also include favorites
old_data_json = """        "stats": {
            p: {"exact": exact[p], "outcomes": outcomes[p], "catches": catches[p]} for p in players
        },"""
new_data_json = """        "stats": {
            p: {"exact": exact[p], "outcomes": outcomes[p], "catches": catches[p]} for p in players
        },
        "favorites_breakdown": {
            p: [{"team": team, "pts": pts, "why": why} for team, pts, why in fav_breakdown[p]] for p in players
        },"""
        
compute_code = compute_code.replace(old_data_json, new_data_json)

with open('compute.py', 'w', encoding='utf-8') as f:
    f.write(compute_code)

print("compute.py updated with favorites_breakdown!")
