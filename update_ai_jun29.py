import json
import os

with open('data/upcoming_ai.json', 'r', encoding='utf-8') as f:
    predictions = json.load(f)

# Clear old R32 predictions if any, but leave others or just overwrite R32-2, R32-3, R32-4
predictions.update({
    "R32-2": {
        "analytics": "Бразилия — фаворит с яркой и изобретательной атакой. Япония — дисциплинированная команда, играющая в высоком темпе. Бразильцам может быть сложно вскрыть организованную оборону самураев, но индивидуальный класс Винисиуса и Родриго должен стать решающим.",
        "predicted_score": [2, 0]
    },
    "R32-3": {
        "analytics": "Германия демонстрирует мощный атакующий футбол, в то время как Парагвай известен своей неуступчивостью и жесткой игрой в отборе. Немцы с первых минут возьмут мяч под свой контроль, и вопрос лишь в том, как долго южноамериканцы смогут выдерживать давление.",
        "predicted_score": [3, 0]
    },
    "R32-4": {
        "analytics": "Одно из самых интересных противостояний. Нидерланды любят доминировать и играть первым номером. Марокко, обладая опытом ЧМ-2022, умеет блестяще защищаться и остро контратаковать. Ожидается тяжелый и вязкий матч, где судьбу путевки может решить всего один гол.",
        "predicted_score": [1, 0]
    }
})

with open('data/upcoming_ai.json', 'w', encoding='utf-8') as f:
    json.dump(predictions, f, ensure_ascii=False, indent=2)

print("upcoming_ai.json updated for June 29 playoff matches!")
