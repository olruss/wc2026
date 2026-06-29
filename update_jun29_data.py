import json
from compute import load, DATA

def main():
    # Update predictions
    preds = load("predictions.json")
    
    oleg_preds = {
        "R32-2": [2, 0],
        "R32-3": [2, 0],
        "R32-4": [2, 1]
    }
    
    alex_preds = {
        "R32-2": [3, 1],
        "R32-3": [2, 1],
        "R32-4": [2, 0]
    }
    
    preds.setdefault("Oleg", {}).update(oleg_preds)
    preds.setdefault("Alex", {}).update(alex_preds)
    
    with open(DATA / "predictions.json", "w", encoding="utf-8") as f:
        json.dump(preds, f, indent=2, ensure_ascii=False)
        
    # Update fixtures
    fixtures = load("fixtures.json")
    for m in fixtures["matches"]:
        if m["id"] == "R32-2":
            m["status"] = "finished"
            m["home_score"] = 2
            m["away_score"] = 1
            
    with open(DATA / "fixtures.json", "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
    print("Predictions for Jun 29 and Brazil vs Japan match result updated.")

if __name__ == "__main__":
    main()
