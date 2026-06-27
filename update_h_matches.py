import json

with open('data/fixtures.json', 'r') as f:
    data = json.load(f)

for m in data['matches']:
    if m['id'] == 'H5':
        m['status'] = 'finished'
        m['home_score'] = 0
        m['away_score'] = 0
    elif m['id'] == 'H6':
        m['status'] = 'finished'
        m['home_score'] = 0
        m['away_score'] = 1

with open('data/fixtures.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated H5 and H6.")
