import json

with open('data/fixtures.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for match in data['matches']:
    if match['id'] == 'I5' and match['away'] == 'France':
        match['away_score'] = 4

with open('data/fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("France score updated to 4")
