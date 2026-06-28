import json

with open('data/predictions.json', 'r', encoding='utf-8') as f:
    preds = json.load(f)

new_alex = {
    "L5": [0, 3],
    "L6": [1, 1],
    "K5": [1, 2],
    "K6": [1, 2],
    "J5": [1, 1],
    "J6": [0, 3]
}

new_oleg = {
    "L5": [0, 2],
    "L6": [2, 1],
    "K5": [1, 2],
    "K6": [2, 0],
    "J5": [1, 2],
    "J6": [0, 3]
}

if "Alex" not in preds:
    preds["Alex"] = {}
if "Oleg" not in preds:
    preds["Oleg"] = {}

preds["Alex"].update(new_alex)
preds["Oleg"].update(new_oleg)

with open('data/predictions.json', 'w', encoding='utf-8') as f:
    json.dump(preds, f, indent=2, ensure_ascii=False)

print("Predictions updated.")
