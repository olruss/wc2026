import re

# 1. Update index.html
with open('docs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add form guide for Oleg
html = html.replace(
    '<div class="stat-item"><span id="stats-catches-Oleg">0</span> зацепов</div>\n                    </div>',
    '<div class="stat-item"><span id="stats-catches-Oleg">0</span> зацепов</div>\n                    </div>\n                    <div class="g-score-form" id="form-Oleg"></div>'
)

# Add form guide for Alex
html = html.replace(
    '<div class="stat-item"><span id="stats-catches-Alex">0</span> зацепов</div>\n                    </div>',
    '<div class="stat-item"><span id="stats-catches-Alex">0</span> зацепов</div>\n                    </div>\n                    <div class="g-score-form text-right" id="form-Alex"></div>'
)

# Add favorites block
favorites_html = """
            <div class="favorites-section">
                <h3>Команды-фавориты</h3>
                <div class="favorites-grid">
                    <div class="favorites-col" id="fav-Oleg"></div>
                    <div class="favorites-col" id="fav-Alex"></div>
                </div>
            </div>
            
            <!-- Навигация -->"""

html = html.replace('<!-- Навигация -->', favorites_html)

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
css_addition = """
/* Полоса удачи */
.g-score-form {
    display: flex;
    gap: 4px;
    margin-top: 8px;
}
.g-score-form.text-right {
    justify-content: flex-end;
}
.form-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}
.dot-green { background-color: var(--color-exact); }
.dot-yellow { background-color: var(--color-outcome); }
.dot-red { background-color: var(--color-catch); }
.dot-grey { background-color: var(--border-color); }

/* Фавориты */
.favorites-section {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
}
.favorites-section h3 {
    margin-top: 0;
    margin-bottom: var(--spacing-md);
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
}
.favorites-grid {
    display: flex;
    justify-content: space-between;
    gap: var(--spacing-md);
}
.favorites-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.fav-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    padding: 4px 8px;
    background: var(--bg-color);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
}
.fav-team {
    font-weight: 500;
}
.fav-pts {
    font-size: 0.75rem;
    color: var(--text-muted);
    background: var(--card-bg);
    padding: 2px 6px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
}
"""

with open('docs/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.g-score-form' not in css:
    with open('docs/style.css', 'a', encoding='utf-8') as f:
        f.write(css_addition)

# 3. Update app.js
js_addition = """
    // Отрисовка полосы удачи (последние 8 матчей)
    if (data.history && data.history.length > 0) {
        const last8 = data.history.slice(-8);
        ['Oleg', 'Alex'].forEach(player => {
            const formContainer = document.getElementById(`form-${player}`);
            if (formContainer) {
                formContainer.innerHTML = '';
                last8.forEach(match => {
                    const pts = match[player];
                    let dotClass = 'dot-grey';
                    if (pts === 6) dotClass = 'dot-green';
                    else if (pts >= 3) dotClass = 'dot-yellow';
                    else if (pts > 0) dotClass = 'dot-red';
                    
                    const dot = document.createElement('span');
                    dot.className = `form-dot ${dotClass}`;
                    dot.title = `${match.matchId}: ${pts} очков`;
                    formContainer.appendChild(dot);
                });
            }
        });
    }

    // Отрисовка фаворитов
    if (data.favorites_breakdown) {
        ['Oleg', 'Alex'].forEach(player => {
            const favContainer = document.getElementById(`fav-${player}`);
            if (favContainer && data.favorites_breakdown[player]) {
                favContainer.innerHTML = '';
                data.favorites_breakdown[player].forEach(fav => {
                    const item = document.createElement('div');
                    item.className = 'fav-item';
                    item.innerHTML = `<span class="fav-team">${fav.team}</span><span class="fav-pts" title="${fav.why}">+${fav.pts}</span>`;
                    favContainer.appendChild(item);
                });
            }
        });
    }
"""

with open('docs/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

if '// Отрисовка полосы удачи' not in js:
    js = js.replace('// Обновление отрыва', js_addition + '\n    // Обновление отрыва')
    with open('docs/app.js', 'w', encoding='utf-8') as f:
        f.write(js)

print("Frontend updated!")
