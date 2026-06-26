import re

# 1. Update index.html
with open('docs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add stats div for Oleg
html = html.replace(
    '<div class="g-score-pts" id="scoreOleg">0</div>\n                </div>',
    '<div class="g-score-pts" id="scoreOleg">0</div>\n                    <div class="player-stats">\n                        <div class="stat-item"><span id="stats-exact-Oleg">0</span> точных</div>\n                        <div class="stat-item"><span id="stats-outcomes-Oleg">0</span> исходов</div>\n                        <div class="stat-item"><span id="stats-catches-Oleg">0</span> зацепов</div>\n                    </div>\n                </div>'
)

# Add stats div for Alex
html = html.replace(
    '<div class="g-score-pts" id="scoreAlex">0</div>\n                </div>',
    '<div class="g-score-pts" id="scoreAlex">0</div>\n                    <div class="player-stats text-right">\n                        <div class="stat-item"><span id="stats-exact-Alex">0</span> точных</div>\n                        <div class="stat-item"><span id="stats-outcomes-Alex">0</span> исходов</div>\n                        <div class="stat-item"><span id="stats-catches-Alex">0</span> зацепов</div>\n                    </div>\n                </div>'
)

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
css_addition = """
.player-stats {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-top: 4px;
}
.player-stats.text-right {
    align-items: flex-end;
}
.stat-item {
    font-size: 0.75rem;
    color: #9aa0a6;
    line-height: 1.2;
}
.stat-item span {
    font-weight: 500;
    color: #e8eaed;
}
"""

with open('docs/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.player-stats' not in css:
    with open('docs/style.css', 'a', encoding='utf-8') as f:
        f.write(css_addition)

# 3. Update app.js
js_addition = """
    // Обновление статистики (Точные, Исходы, Зацепы)
    if (data.stats) {
        animateValue("stats-exact-Oleg", 0, data.stats.Oleg.exact, 1000);
        animateValue("stats-outcomes-Oleg", 0, data.stats.Oleg.outcomes, 1000);
        animateValue("stats-catches-Oleg", 0, data.stats.Oleg.catches, 1000);
        
        animateValue("stats-exact-Alex", 0, data.stats.Alex.exact, 1000);
        animateValue("stats-outcomes-Alex", 0, data.stats.Alex.outcomes, 1000);
        animateValue("stats-catches-Alex", 0, data.stats.Alex.catches, 1000);
    }
"""

with open('docs/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

if '// Обновление статистики (Точные, Исходы, Зацепы)' not in js:
    js = js.replace('// Обновление отрыва', js_addition + '\n    // Обновление отрыва')
    with open('docs/app.js', 'w', encoding='utf-8') as f:
        f.write(js)

print("HTML, CSS and JS updated!")
