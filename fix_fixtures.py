import json

with open('data/fixtures.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for match in data['matches']:
    if match['id'] == 'G5':
        match['status'] = 'scheduled'
        match['home_score'] = None
        match['away_score'] = None
    elif match['id'] == 'G6':
        match['status'] = 'scheduled'
        match['home_score'] = None
        match['away_score'] = None
    elif match['id'] == 'I5':
        match['status'] = 'finished'
        match['home_score'] = 1
        match['away_score'] = 3
    elif match['id'] == 'I6':
        match['status'] = 'finished'
        match['home_score'] = 5
        match['away_score'] = 0

with open('data/fixtures.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixtures fixed!")
