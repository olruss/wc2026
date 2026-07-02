import json
from compute import load, DATA

def main():
    preds = load("predictions.json")
    
    # R32-5: Ivory Coast vs Norway
    # R32-6: France vs Sweden
    # R32-7: Mexico vs Ecuador
    # R32-8: England vs DR Congo
    # R32-9: Belgium vs Senegal
    # R32-10: United States vs Bosnia and Herzegovina

    oleg_preds = {
        "R32-5": [1, 2],
        "R32-6": [2, 0],
        "R32-7": [2, 1],
        "R32-8": [3, 1],
        "R32-9": [3, 2],
        "R32-10": [2, 0]
    }
    
    alex_preds = {
        "R32-5": [1, 3],
        "R32-6": [3, 0],
        "R32-7": [2, 0],
        "R32-8": [2, 0],
        "R32-9": [2, 1],
        "R32-10": [3, 1]
    }
    
    preds.setdefault("Oleg", {}).update(oleg_preds)
    preds.setdefault("Alex", {}).update(alex_preds)
    
    with open(DATA / "predictions.json", "w", encoding="utf-8") as f:
        json.dump(preds, f, indent=2, ensure_ascii=False)
        
    print("Predictions for Jun 30 and Jul 1 matches updated.")

if __name__ == "__main__":
    main()
