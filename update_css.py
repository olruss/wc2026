import re

with open('docs/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Remove blobs
css = re.sub(r'/\* Декоративные пятна на фоне \*/.*?@keyframes float \{.*?\}', '', css, flags=re.DOTALL)

# 2. Change container to flat dark
container_new = '''
.container {
    background: #202124;
    border-radius: 12px;
    padding: 20px 0;
    width: 100%;
    max-width: 900px;
}
'''
css = re.sub(r'\.container \{.*?\opacity: 0;\n    transform: translateY\(20px\);\n\}', container_new, css, flags=re.DOTALL)
css = re.sub(r'@keyframes fadeUp \{.*?\}', '', css, flags=re.DOTALL)

# 3. Add Google Tabs & Scoreboard styles
g_styles = '''
/* Google Style Tabs */
.g-tabs {
    display: flex;
    justify-content: center;
    border-bottom: 1px solid #3c4043;
    margin-bottom: 30px;
    padding: 0 20px;
}
.g-tab-btn {
    background: transparent;
    border: none;
    color: #9aa0a6;
    font-size: 1rem;
    font-weight: 500;
    padding: 12px 24px;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: color 0.2s, border-color 0.2s;
}
.g-tab-btn:hover {
    color: #e8eaed;
}
.g-tab-btn.active {
    color: #8ab4f8;
    border-bottom-color: #8ab4f8;
}

/* Google Style Scoreboard */
.g-scoreboard {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #303134;
    border: 1px solid #3c4043;
    border-radius: 8px;
    padding: 20px 30px;
    margin: 0 20px 30px 20px;
}
.g-score-player {
    display: flex;
    flex-direction: column;
}
.g-score-player.text-right {
    text-align: right;
    align-items: flex-end;
}
.g-score-name {
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 4px;
}
.g-score-pts {
    font-size: 2.5rem;
    font-weight: 700;
    color: #e8eaed;
    line-height: 1;
}
.g-score-divider {
    flex: 1;
    text-align: center;
    display: flex;
    justify-content: center;
}
.g-score-gap {
    background: rgba(255,255,255,0.08);
    color: #9aa0a6;
    padding: 6px 16px;
    border-radius: 16px;
    font-size: 0.85rem;
    font-weight: 500;
}
@media (max-width: 600px) {
    .g-scoreboard {
        padding: 15px;
    }
    .g-score-pts { font-size: 2rem; }
    .g-score-gap { padding: 4px 10px; font-size: 0.75rem; }
    .g-tabs { padding: 0; }
    .g-tab-btn { padding: 12px 16px; font-size: 0.9rem; }
}
'''
css = css.replace('header {\n    text-align: center;', g_styles + '\nheader {\n    text-align: center;')

# 4. Remove old scoreboard and player-card styles
css = re.sub(r'\.score-board \{.*?\@media \(max-width: 600px\) \{.*?\n\}', '@media (max-width: 600px) {\n}', css, flags=re.DOTALL)

# 5. Clean up Match Card to be flatter
css = re.sub(r'\.match-card \{.*?\}', '.match-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid #3c4043; }\n.match-card:last-child { border-bottom: none; }', css, flags=re.DOTALL)
css = re.sub(r'\.match-card:hover \{.*?\}', '', css, flags=re.DOTALL)

with open('docs/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("CSS updated!")
