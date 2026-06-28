import json
import os

with open('data/upcoming_ai.json', 'r', encoding='utf-8') as f:
    predictions = json.load(f)

# Keep R32-1 (South Africa vs Canada) since it's the only one on June 28
predictions = {
    "R32-1": {
        "analytics": "Первый матч плей-офф! Канада показывает невероятно быстрый и интенсивный футбол с акцентом на фланги, где сияет Альфонсо Дэвис. Южная Африка играет более дисциплинированно и компактно, уповая на стандарты и контратаки. Ожидается равная игра, но североамериканцы выглядят чуть свежее и острее в завершении.",
        "predicted_score": [0, 2]
    }
}

with open('data/upcoming_ai.json', 'w', encoding='utf-8') as f:
    json.dump(predictions, f, ensure_ascii=False, indent=2)

print("upcoming_ai.json updated for the single June 28 playoff match!")
