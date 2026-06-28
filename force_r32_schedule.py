import json
from compute import load, DATA

def main():
    fixtures = load("fixtures.json")
    matches = fixtures["matches"]
    
    r32_schedule = [
        ("South Africa", "Canada", "2026-06-28T19:00:00Z"),
        ("Brazil", "Japan", "2026-06-29T17:00:00Z"),
        ("Germany", "Paraguay", "2026-06-29T20:30:00Z"),
        ("Netherlands", "Morocco", "2026-06-30T01:00:00Z"),
        ("Ivory Coast", "Norway", "2026-06-30T17:00:00Z"),
        ("France", "Sweden", "2026-06-30T21:00:00Z"),
        ("Mexico", "Ecuador", "2026-07-01T01:00:00Z"),
        ("England", "DR Congo", "2026-07-01T16:00:00Z"),
        ("Belgium", "Senegal", "2026-07-01T20:00:00Z"),
        ("United States", "Bosnia and Herzegovina", "2026-07-02T00:00:00Z"),
        ("Spain", "TBD", "2026-07-02T19:00:00Z"),
        ("Portugal", "Croatia", "2026-07-02T23:00:00Z"),
        ("Switzerland", "TBD", "2026-07-03T03:00:00Z"),
        ("Australia", "Egypt", "2026-07-03T18:00:00Z"),
        ("Argentina", "Cape Verde", "2026-07-03T22:00:00Z"),
        ("Colombia", "Ghana", "2026-07-04T01:30:00Z")
    ]
    
    r32_idx = 0
    for m in matches:
        if m["stage"] == "round_of_32":
            if r32_idx < len(r32_schedule):
                home, away, dt = r32_schedule[r32_idx]
                m["home"] = home
                m["away"] = away
                m["datetime_utc"] = dt
                r32_idx += 1
                
    # Write back
    with open(DATA / "fixtures.json", "w") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print(f"Updated {r32_idx} R32 matches based on explicit user schedule.")

if __name__ == "__main__":
    main()
