import json
from compute import calculate_groups, load, DATA

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
    
    for g, teams in finished_groups.items():
        winner = teams[0]["team"]
        runner_up = teams[1]["team"]
        print(f"Group {g}: Winner = {winner}, Runner-up = {runner_up}")
        
        # Replace placeholders in fixtures
        for m in matches:
            if m["stage"] != "group":
                if m["home"] == f"Winner Grp {g}":
                    m["home"] = winner
                if m["away"] == f"Winner Grp {g}":
                    m["away"] = winner
                if m["home"] == f"Runner-up Grp {g}":
                    m["home"] = runner_up
                if m["away"] == f"Runner-up Grp {g}":
                    m["away"] = runner_up

    # Write back
    with open(DATA / "fixtures.json", "w") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
if __name__ == "__main__":
    main()
