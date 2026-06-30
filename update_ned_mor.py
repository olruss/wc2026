import json
from compute import load, DATA

def main():
    fixtures = load("fixtures.json")
    
    for m in fixtures["matches"]:
        if m["id"] == "R32-4": # Netherlands vs Morocco
            m["status"] = "finished"
            m["home_score"] = 1
            m["away_score"] = 1
            m["decided_by"] = "penalties"
            m["shootout_winner"] = "Morocco"
            
    with open(DATA / "fixtures.json", "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print("R32-4 updated with Morocco penalty win.")

if __name__ == "__main__":
    main()
