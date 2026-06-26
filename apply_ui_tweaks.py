import re

with open('docs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add crown HTML
html = html.replace(
    '<div class="g-score-name" style="color: var(--color-oleg);">Олег</div>',
    '<div class="crown" id="crownOleg"></div>\n                    <div class="g-score-name" style="color: var(--color-oleg);">Олег</div>'
)

html = html.replace(
    '<div class="g-score-name" style="color: var(--color-alex);">Алекс</div>',
    '<div class="crown" id="crownAlex"></div>\n                    <div class="g-score-name" style="color: var(--color-alex);">Алекс</div>'
)

# 2. Extract favorites section
fav_section_match = re.search(r'<div class="favorites-section">[\s\S]*?</div>\s*</div>\s*', html)
if fav_section_match:
    fav_html = fav_section_match.group(0)
    html = html.replace(fav_html, '')
    
    # Add new tab
    new_tab = f"""
        <!-- Вкладка Фавориты -->
        <div id="tab-favorites" class="tab-content" style="display: none;">
            {fav_html}
        </div>
"""
    # Insert after tab-predictions
    html = html.replace('        <!-- Вкладка Прогнозы -->', new_tab + '\n        <!-- Вкладка Прогнозы -->')
    
    # Add tab button
    html = html.replace('<button class="g-tab-btn" onclick="switchTab(\'groups\')">Группы</button>',
                        '<button class="g-tab-btn" onclick="switchTab(\'favorites\')">Фавориты</button>\n            <button class="g-tab-btn" onclick="switchTab(\'groups\')">Группы</button>')


with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# Update JS
with open('docs/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_gap_js = """
    // Обновление отрыва
    const gap = Math.abs(scoreOleg - scoreAlex);
    let leader = "Ничья";
    if (scoreOleg > scoreAlex) leader = "Олег";
    else if (scoreAlex > scoreOleg) leader = "Алекс";
    
    const gapElement = document.getElementById('gapText');
    if (gap === 0) {
        gapElement.textContent = "Счет равный";
    } else {
        gapElement.textContent = `${leader} +${gap}`;
    }

    // Корона
    const crownOleg = document.getElementById('crownOleg');
    const crownAlex = document.getElementById('crownAlex');
    if (crownOleg && crownAlex) {
        crownOleg.textContent = scoreOleg > scoreAlex ? '👑' : '';
        crownAlex.textContent = scoreAlex > scoreOleg ? '👑' : '';
    }
"""

js = re.sub(r'// Обновление отрыва[\s\S]*?\}', new_gap_js.strip(), js)

with open('docs/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update CSS
with open('docs/style.css', 'a', encoding='utf-8') as f:
    f.write('\n.crown { font-size: 1.2rem; height: 1.2rem; line-height: 1; text-align: center; margin-bottom: 2px; }')

print("UI applied!")
