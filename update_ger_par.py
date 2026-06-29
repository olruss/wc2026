import json
from compute import load, DATA

def main():
    fixtures = load("fixtures.json")
    
    for m in fixtures["matches"]:
        if m["id"] == "R32-3": # Germany vs Paraguay
            m["status"] = "finished"
            m["home_score"] = 1
            m["away_score"] = 1
            m["decided_by"] = "penalties"
            m["shootout_winner"] = "Paraguay"
            
    with open(DATA / "fixtures.json", "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print("R32-3 updated with penalty shootout result.")

if __name__ == "__main__":
    main()
