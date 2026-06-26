import re

with open('docs/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add a call to renderUpcoming in updateUI
if 'renderUpcoming(data);' not in js:
    js = js.replace('renderHistory(data.history);', 'renderHistory(data.history);\n    renderUpcoming(data);')

# Append upcoming match logic
upcoming_logic = """

// --- ПРОГНОЗЫ (UPCOMING) ---
let userPredictions = {};

function renderUpcoming(data) {
    const list = document.getElementById('upcomingList');
    if (!list) return;
    list.innerHTML = '';
    
    if (!data.upcoming || data.upcoming.length === 0) {
        list.innerHTML = '<p style="text-align:center; color: var(--text-muted);">Нет предстоящих матчей</p>';
        return;
    }
    
    data.upcoming.forEach(match => {
        const id = match.id;
        const aiData = (data.upcoming_ai && data.upcoming_ai[id]) || {};
        const aiScore = aiData.predicted_score || [0, 0];
        
        // Инициализируем локальный стейт прогноза, если еще нет
        if (!userPredictions[id]) {
            userPredictions[id] = [...aiScore];
        }
        const currentScore = userPredictions[id];
        
        const card = document.createElement('div');
        card.className = 'upcoming-card';
        
        // Парсим дату
        const d = match.datetime_utc ? new Date(match.datetime_utc) : null;
        let dateStr = 'TBD';
        if (d && !isNaN(d.getTime())) {
            dateStr = d.toLocaleDateString('ru-RU', {day: 'numeric', month: 'short', hour: '2-digit', minute:'2-digit'});
        }
        
        card.innerHTML = `
            <div class="upcoming-info">
                <div class="match-id">${match.id} &middot; ${dateStr}</div>
            </div>
            <div class="upcoming-teams">
                ${match.home || 'TBD'} &mdash; ${match.away || 'TBD'}
            </div>
            <div class="upcoming-analytics">
                🤖 <i>${aiData.analytics || 'Ожидаем интересный матч.'}</i>
            </div>
            <div class="score-editor">
                <div class="score-team">
                    <button class="score-btn" onclick="changeScore('${id}', 0, -1)">-</button>
                    <div class="score-val" id="score-${id}-0">${currentScore[0]}</div>
                    <button class="score-btn" onclick="changeScore('${id}', 0, 1)">+</button>
                </div>
                <span style="font-weight: 700; color: #5f6368;">:</span>
                <div class="score-team">
                    <button class="score-btn" onclick="changeScore('${id}', 1, -1)">-</button>
                    <div class="score-val" id="score-${id}-1">${currentScore[1]}</div>
                    <button class="score-btn" onclick="changeScore('${id}', 1, 1)">+</button>
                </div>
            </div>
        `;
        list.appendChild(card);
    });
}

function changeScore(matchId, teamIdx, delta) {
    let score = userPredictions[matchId][teamIdx];
    score += delta;
    if (score < 0) score = 0;
    userPredictions[matchId][teamIdx] = score;
    document.getElementById(`score-${matchId}-${teamIdx}`).textContent = score;
}

function shareToTelegram() {
    if (!window.dashboardData || !window.dashboardData.upcoming) return;
    
    let text = "Мои прогнозы на завтра:\\n\\n";
    let hasPredictions = false;
    
    window.dashboardData.upcoming.forEach(match => {
        const score = userPredictions[match.id];
        if (score) {
            hasPredictions = true;
            text += `${match.home || 'TBD'} ${score[0]}:${score[1]} ${match.away || 'TBD'}\\n`;
        }
    });
    
    if (!hasPredictions) {
        alert('Нет предстоящих матчей для прогноза.');
        return;
    }
    
    // Формируем URL для Telegram
    const encodedText = encodeURIComponent(text);
    const tgUrl = `https://t.me/share/url?url=&text=${encodedText}`;
    
    // Открываем Telegram
    window.open(tgUrl, '_blank');
}
"""

if '// --- ПРОГНОЗЫ (UPCOMING) ---' not in js:
    with open('docs/app.js', 'a', encoding='utf-8') as f:
        f.write(upcoming_logic)

with open('docs/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
    if '// --- ПРОГНОЗЫ (UPCOMING) ---' not in js:
        f.write(upcoming_logic)

print("app.js updated!")
