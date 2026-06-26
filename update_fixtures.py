import json

with open('data/fixtures.json', 'r', encoding='utf-8') as f:
    fixtures = json.load(f)

for match in fixtures['matches']:
    if match['id'] == 'G5':
        match['status'] = 'finished'
        match['home_score'] = 2
        match['away_score'] = 1
    elif match['id'] == 'G6':
        match['status'] = 'finished'
        match['home_score'] = 0
        match['away_score'] = 3

with open('data/fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(fixtures, f, indent=2, ensure_ascii=False)

print("fixtures updated!")
