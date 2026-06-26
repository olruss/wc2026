import re

# 1. Update index.html
with open('docs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<section id="predictions-tab" class="tab-content" style="display: none;">', '<div id="tab-predictions" class="tab-content">')
html = html.replace('</section>\n        <footer>', '</div>\n        <footer>')

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
css_addition = """
.predictions-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 20px;
}
.tg-share-btn {
    background-color: #2481cc;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: background-color 0.2s;
}
.tg-share-btn:hover { background-color: #1d69a6; }
.upcoming-card {
    background: #202124;
    border: 1px solid #3c4043;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 15px;
}
.upcoming-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.upcoming-teams {
    font-size: 1.1rem;
    font-weight: 500;
}
.upcoming-date {
    font-size: 0.8rem;
    color: #9aa0a6;
}
.upcoming-analytics {
    font-size: 0.85rem;
    color: #bdc1c6;
    margin-bottom: 16px;
    line-height: 1.4;
}
.score-editor {
    display: flex;
    align-items: center;
    gap: 12px;
}
.score-team {
    display: flex;
    align-items: center;
    gap: 8px;
}
.score-btn {
    background: #303134;
    border: 1px solid #5f6368;
    color: #e8eaed;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
}
.score-btn:hover { background: #3c4043; }
.score-val {
    font-size: 1.2rem;
    font-weight: 700;
    min-width: 20px;
    text-align: center;
}
"""

with open('docs/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.predictions-header' not in css:
    with open('docs/style.css', 'a', encoding='utf-8') as f:
        f.write(css_addition)

print("HTML/CSS updated!")
