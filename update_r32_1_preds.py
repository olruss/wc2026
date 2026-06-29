import json

with open('data/predictions.json', 'r', encoding='utf-8') as f:
    preds = json.load(f)

# Match R32-1 is South Africa (Home) vs Canada (Away)
# User: Canada 2 - 0 South Africa -> South Africa 0 - 2 Canada
# Alex: Canada 2 - 1 South Africa -> South Africa 1 - 2 Canada
new_oleg = {"R32-1": [0, 2]}
new_alex = {"R32-1": [1, 2]}

if "Oleg" not in preds:
    preds["Oleg"] = {}
if "Alex" not in preds:
    preds["Alex"] = {}

preds["Oleg"].update(new_oleg)
preds["Alex"].update(new_alex)

with open('data/predictions.json', 'w', encoding='utf-8') as f:
    json.dump(preds, f, indent=2, ensure_ascii=False)

print("Predictions updated for R32-1.")
