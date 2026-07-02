import json
from compute import load, DATA

def main():
    fixtures = load("fixtures.json")
    
    results = {
        "R32-5": (1, 2), # Ivory Coast 1 - 2 Norway
        "R32-6": (3, 0), # France 3 - 0 Sweden
        "R32-7": (2, 0), # Mexico 2 - 0 Ecuador
        "R32-8": (2, 1), # England 2 - 1 DR Congo
        "R32-9": (3, 2), # Belgium 3 - 2 Senegal
        "R32-10": (2, 0) # USA 2 - 0 Bosnia and Herzegovina
    }
    
    for m in fixtures["matches"]:
        if m["id"] in results:
            m["status"] = "finished"
            m["home_score"] = results[m["id"]][0]
            m["away_score"] = results[m["id"]][1]
            
    with open(DATA / "fixtures.json", "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print("R32-5 through R32-10 updated with final scores.")

if __name__ == "__main__":
    main()
