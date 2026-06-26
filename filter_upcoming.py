import re

with open('docs/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = """function renderUpcoming(data) {
    const list = document.getElementById('upcomingList');
    if (!list) return;
    list.innerHTML = '';
    
    if (!data.upcoming || data.upcoming.length === 0) {
        list.innerHTML = '<p style="text-align:center; color: var(--text-muted);">Нет предстоящих матчей</p>';
        return;
    }
    
    // Оставляем только матчи ближайшего игрового дня
    const sorted = [...data.upcoming].sort((a, b) => new Date(a.datetime_utc) - new Date(b.datetime_utc));
    const firstDate = new Date(sorted[0].datetime_utc).toDateString();
    data.upcoming = sorted.filter(m => new Date(m.datetime_utc).toDateString() === firstDate);
"""

# Replace the beginning of renderUpcoming
js = re.sub(
    r"function renderUpcoming\(data\) \{[\s\S]*?if \(\!data\.upcoming \|\| data\.upcoming\.length === 0\) \{[\s\S]*?return;\n    \}",
    replacement,
    js,
    count=1
)

with open('docs/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("app.js updated with date filter!")
