import json
from compute import calculate_groups, load, DATA
from datetime import datetime, timedelta

def main():
    fixtures = load("fixtures.json")
    matches = fixtures["matches"]
    
    # Calculate group standings
    groups = calculate_groups(matches)
    
    # Find finished groups
    finished_groups = {}
    for g, teams in groups.items():
        # Check if all matches in this group are finished
        group_matches = [m for m in matches if m.get("group") == g]
        if all(m["status"] == "finished" for m in group_matches) and len(group_matches) > 0:
            finished_groups[g] = teams
    
    # Check if we have all 12 groups finished
    if len(finished_groups) < 12:
        print("Not all groups are finished yet. Using available data...")
    
    winners = {}
    runners_up = {}
    thirds = []
    
    for g, teams in finished_groups.items():
        winners[g] = teams[0]["team"]
        runners_up[g] = teams[1]["team"]
        if len(teams) > 2:
            thirds.append({
                "team": teams[2]["team"],
                "group": g,
                "pts": teams[2]["pts"],
                "gd": teams[2]["gd"],
                "gf": teams[2]["gf"]
            })
            
    # Sort thirds by pts, gd, gf (descending)
    thirds.sort(key=lambda x: (x["pts"], x["gd"], x["gf"]), reverse=True)
    best_thirds = [t["team"] for t in thirds[:8]]
    
    def get_team(mapping_str):
        parts = mapping_str.split(" ")
        if parts[0] == "W":
            return winners.get(parts[1], f"Winner Grp {parts[1]}")
        elif parts[0] == "RU":
            return runners_up.get(parts[1], f"Runner-up Grp {parts[1]}")
        elif parts[0] == "3rd":
            if best_thirds:
                return best_thirds.pop(0) # sequentially pop the best thirds
            return "Best 3rd Team"
        return mapping_str

    # Official R32 Matchups (Simplified 3rd place mapping)
    r32_mapping = {
        "R32-1":  ("RU A", "RU B"),        # Match 73
        "R32-2":  ("W E", "3rd"),          # Match 74
        "R32-3":  ("W F", "RU C"),         # Match 75
        "R32-4":  ("W C", "RU F"),         # Match 76
        "R32-5":  ("W I", "3rd"),          # Match 77
        "R32-6":  ("RU E", "RU I"),        # Match 78
        "R32-7":  ("W A", "3rd"),          # Match 79
        "R32-8":  ("W L", "3rd"),          # Match 80
        "R32-9":  ("W D", "3rd"),          # Match 81
        "R32-10": ("W G", "3rd"),          # Match 82
        "R32-11": ("RU K", "RU L"),        # Match 83
        "R32-12": ("W H", "RU J"),         # Match 84
        "R32-13": ("W B", "3rd"),          # Match 85
        "R32-14": ("W J", "RU H"),         # Match 86
        "R32-15": ("W K", "3rd"),          # Match 87
        "R32-16": ("RU D", "RU G")         # Match 88
    }

    # Dates for R32: June 28 to July 3 (matches 73-88, approx 2-3 matches per day)
    # We will just assign them incrementally starting June 28 14:00Z
    base_date = datetime(2026, 6, 28, 14, 0, 0)
    
    r32_index = 0
    for m in matches:
        if m["stage"] == "round_of_32":
            mapping = r32_mapping.get(m["id"])
            if mapping:
                m["home"] = get_team(mapping[0])
                m["away"] = get_team(mapping[1])
                
                # Assign specific times to spread them across 6 days
                days_offset = r32_index // 3
                hours_offset = (r32_index % 3) * 4 # 14:00, 18:00, 22:00
                m_date = base_date + timedelta(days=days_offset, hours=hours_offset)
                m["datetime_utc"] = m_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            r32_index += 1

    # Write back
    with open(DATA / "fixtures.json", "w") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print("Playoffs updated with official 2026 World Cup bracket (Matches 73-88)!")

if __name__ == "__main__":
    main()
