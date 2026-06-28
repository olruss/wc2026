import json

with open('data/fixtures.json', 'r') as f:
    data = json.load(f)

results = {
    'G5': (1, 1), # Egypt 1 - 1 Iran
    'G6': (1, 5), # New Zealand 1 - 5 Belgium
    'K5': (0, 0), # Colombia 0 - 0 Portugal
    'K6': (3, 1), # DR Congo 3 - 1 Uzbekistan
    'L5': (0, 2), # Panama 0 - 2 England
    'L6': (2, 1)  # Croatia 2 - 1 Ghana
}

for m in data['matches']:
    if m['id'] in results:
        m['status'] = 'finished'
        m['home_score'], m['away_score'] = results[m['id']]

with open('data/fixtures.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated 6 matches.")
