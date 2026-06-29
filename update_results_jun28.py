import json
from compute import load, DATA

def main():
    fixtures = load("fixtures.json")
    matches = fixtures["matches"]
    
    results = {
        "J5": (3, 3), # Algeria 3 - 3 Austria
        "J6": (1, 3), # Jordan 1 - 3 Argentina
        "R32-1": (0, 1) # South Africa 0 - 1 Canada
    }
    
    for m in matches:
        if m["id"] in results:
            m["status"] = "finished"
            m["home_score"] = results[m["id"]][0]
            m["away_score"] = results[m["id"]][1]
            
    with open(DATA / "fixtures.json", "w") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print("Match results updated for J5, J6, and R32-1.")

if __name__ == "__main__":
    main()
