import re

with open('compute.py', 'r', encoding='utf-8') as f:
    compute_code = f.read()

# 1. Add `catches = {p: 0 for p in players}`
compute_code = compute_code.replace('    outcomes = {p: 0 for p in players}\n', '    outcomes = {p: 0 for p in players}\n    catches = {p: 0 for p in players}\n')

# 2. Update logic for exact, outcomes, catches
old_logic = """            if pts == sum(scoring.values()):
                exact[p] += 1
            if "O" in detail:
                outcomes[p] += 1"""
new_logic = """            if pts == sum(scoring.values()):
                exact[p] += 1
            elif "O" in detail:
                outcomes[p] += 1
            elif pts > 0:
                catches[p] += 1"""
compute_code = compute_code.replace(old_logic, new_logic)

# 3. Add to output
compute_code = compute_code.replace('f"(exact: {exact[p]}, outcomes: {outcomes[p]})")', 'f"(exact: {exact[p]}, outcomes: {outcomes[p]}, catches: {catches[p]})")')

# 4. Add stats to data_json
old_data_json = """        "currentScores": {
            p: totals[p] for p in players
        },"""
new_data_json = """        "currentScores": {
            p: totals[p] for p in players
        },
        "stats": {
            p: {"exact": exact[p], "outcomes": outcomes[p], "catches": catches[p]} for p in players
        },"""
compute_code = compute_code.replace(old_data_json, new_data_json)

with open('compute.py', 'w', encoding='utf-8') as f:
    f.write(compute_code)

print("compute.py updated!")
