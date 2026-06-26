document.addEventListener('DOMContentLoaded', () => {
    try {
        if (!window.DASHBOARD_DATA) {
            throw new Error("DASHBOARD_DATA is missing. Ensure data.js is loaded.");
        }
        const data = window.DASHBOARD_DATA;
        
        updateUI(data);
        initChart(data);
        renderMatches(data);
        if (data.groups) renderGroups(data.groups, data.matchDetails);
        if (data.playoffs) renderPlayoffs(data.playoffs);
        if (data.upcoming) renderUpcoming(data);
    } catch (error) {
        console.error("Ошибка инициализации:", error);
        document.getElementById('gapText').textContent = "Ошибка загрузки данных";
    }
});

function updateUI(data) {
    const scoreOleg = data.currentScores.Oleg;
    const scoreAlex = data.currentScores.Alex;
    
    // Анимация набора очков
    animateValue("scoreOleg", 0, scoreOleg, 1000);
    animateValue("scoreAlex", 0, scoreAlex, 1000);
    
    
    // Обновление статистики (Точные, Исходы, Зацепы)
    if (data.stats) {
        animateValue("stats-exact-Oleg", 0, data.stats.Oleg.exact, 1000);
        animateValue("stats-outcomes-Oleg", 0, data.stats.Oleg.outcomes, 1000);
        animateValue("stats-catches-Oleg", 0, data.stats.Oleg.catches, 1000);
        
        animateValue("stats-exact-Alex", 0, data.stats.Alex.exact, 1000);
        animateValue("stats-outcomes-Alex", 0, data.stats.Alex.outcomes, 1000);
        animateValue("stats-catches-Alex", 0, data.stats.Alex.catches, 1000);
    }

    // Обновление отрыва
    const gap = Math.abs(scoreOleg - scoreAlex);
    const leader = scoreOleg > scoreAlex ? "Олег" : (scoreAlex > scoreOleg ? "Алекс" : "Ничья");
    
    const gapElement = document.getElementById('gapText');
    if (gap === 0) {
        gapElement.textContent = "Счет равный";
    } else {
        gapElement.textContent = `Отрыв: ${gap} очков (${leader} впереди)`;
    }

    // Обновление даты
    if (data.lastUpdated) {
        document.getElementById('lastUpdated').textContent = data.lastUpdated;
    }
}

// Простая функция для анимации цифр
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        // easeOutQuart
        const easeProgress = 1 - Math.pow(1 - progress, 4);
        obj.innerHTML = Math.floor(easeProgress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            obj.innerHTML = end; // Финальное точное значение
        }
    };
    window.requestAnimationFrame(step);
}

function initChart(data) {
    const ctx = document.getElementById('pointsChart').getContext('2d');
    
    // Получаем стили из CSS (oklch цвета могут не поддерживаться canvas напрямую во всех браузерах, 
    // поэтому используем hex/rgba fallback или парсим если нужно. В ChartJS лучше передать HEX/RGB).
    // Для безопасности хардкодим fallback цвета, которые выглядят идентично
    const colorOleg = '#3b82f6'; // blue-500
    const colorAlex = '#ef4444'; // red-500

    // Формируем историю. 
    // data.history - массив объектов: { matchId: "E1", Oleg: 3, Alex: 3 }
    
    // Считаем кумулятивную сумму
    let labels = ['Старт'];
    let olegData = [0];
    let alexData = [0];
    
    let currentOleg = 0;
    let currentAlex = 0;

    data.history.forEach(item => {
        labels.push(item.matchId);
        currentOleg += item.Oleg;
        currentAlex += item.Alex;
        olegData.push(currentOleg);
        alexData.push(currentAlex);
    });

    // Настраиваем градиенты для заливки
    const gradientOleg = ctx.createLinearGradient(0, 0, 0, 400);
    gradientOleg.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
    gradientOleg.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    const gradientAlex = ctx.createLinearGradient(0, 0, 0, 400);
    gradientAlex.addColorStop(0, 'rgba(239, 68, 68, 0.4)');
    gradientAlex.addColorStop(1, 'rgba(239, 68, 68, 0.0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Олег',
                    data: olegData,
                    borderColor: colorOleg,
                    backgroundColor: gradientOleg,
                    borderWidth: 2,
                    tension: 0.2,
                    fill: false,
                    pointBackgroundColor: colorOleg,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 0,
                    pointHitRadius: 10,
                    pointHoverRadius: 6
                },
                {
                    label: 'Алекс',
                    data: alexData,
                    borderColor: colorAlex,
                    backgroundColor: gradientAlex,
                    borderWidth: 2,
                    tension: 0.2,
                    fill: false,
                    pointBackgroundColor: colorAlex,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 0,
                    pointHitRadius: 10,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: false // Мы уже показываем легенду в карточках
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#ccc',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            if (context[0].label === 'Старт') return 'До начала турнира';
                            return 'После матча ' + context[0].label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#8b92a5',
                        font: { family: "'Inter', sans-serif" }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#9aa0a6',
                        maxRotation: 45,
                        minRotation: 45,
                        font: { family: "'Inter', sans-serif", size: 10 }
                    }
                } }
        }
    });
}

function renderMatches(data) {
    const list = document.getElementById('matchesList');
    if (!data.matchDetails || data.matchDetails.length === 0) return;

    // Берем последние 20 завершенных матчей (самые свежие сверху)
    const matches = [...data.matchDetails].reverse().slice(0, 20);

    matches.forEach(m => {
        const getPtsClass = (pts) => {
            if (pts >= 4) return 'pts-high';
            if (pts > 0) return 'pts-med';
            return 'pts-low';
        };

        const card = document.createElement('div');
        card.className = 'match-card';
        card.innerHTML = `
            <div class="match-info">
                <div class="match-id">${m.id} • ${m.stage.replace(/_/g, ' ')}</div>
                <div class="match-title">${m.match}</div>
            </div>
            <div class="match-predictions">
                <div class="pred-block">
                    <div class="pred-player oleg">Олег</div>
                    <div class="pred-value">
                        ${m.Oleg_pred} <span class="pred-pts ${getPtsClass(m.Oleg_pts)}">+${m.Oleg_pts}</span>
                    </div>
                </div>
                <div class="pred-block">
                    <div class="pred-player alex">Алекс</div>
                    <div class="pred-value">
                        ${m.Alex_pred} <span class="pred-pts ${getPtsClass(m.Alex_pts)}">+${m.Alex_pts}</span>
                    </div>
                </div>
            </div>
        `;
        list.appendChild(card);
    });
}

function switchTab(tabId) {
    // Убираем класс active у всех кнопок
    document.querySelectorAll('.g-tab-btn').forEach(btn => btn.classList.remove('active'));
    // Добавляем класс active нажатой кнопке
    document.querySelector(`button[onclick="switchTab('${tabId}')"]`).classList.add('active');
    
    // Скрываем все табы
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    // Показываем нужный
    document.getElementById(`tab-${tabId}`).classList.add('active');
}

function renderGroups(groups, matchDetails) {
    const container = document.getElementById('groupsContainer');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Вспомогательная функция для генерации трехбуквенного кода команды
    const getTeamCode = (teamName) => {
        // Простой вариант - первые 3 буквы, в реальном проекте лучше использовать словарь
        return teamName.substring(0, 3).toUpperCase();
    };
    
    for (const [groupName, teams] of Object.entries(groups)) {
        const card = document.createElement('div');
        card.className = 'group-wrapper';
        
        // Массив команд в текущей группе
        const groupTeams = teams.map(t => t.team);
        const groupMatches = (matchDetails || []).filter(m => m.stage === 'group' && m.id.startsWith(groupName));
        
        // Заголовки таблицы: Команда, 4 Команды (Матрица), Статистика
        let thMatrix = '';
        teams.forEach(t => {
            thMatrix += `<th class="matrix-col" title="${t.team}">${getTeamCode(t.team)}</th>`;
        });
        
        let rowsHtml = '';
        teams.forEach((rowTeam, rowIndex) => {
            const rowClass = rowIndex < 2 ? 'qualifier' : '';
            
            // Ячейки матрицы
            let tdMatrix = '';
            teams.forEach((colTeam, colIndex) => {
                if (rowIndex === colIndex) {
                    tdMatrix += `<td class="matrix-col matrix-diagonal"></td>`;
                } else {
                    // Ищем матч между rowTeam и colTeam
                    const match = groupMatches.find(m => 
                        (m.match.includes(rowTeam.team) && m.match.includes(colTeam.team))
                    );
                    
                    if (match) {
                        // Определяем, кто дома, кто в гостях в реальном счете
                        const [mHome, mAway] = match.match.split(' - '); // Если формат "Команда 2-0 Команда", сложно распарсить.
                        // Благо в data.js match имеет формат "Mexico 2-0 South Africa"
                        const matchParts = match.match.match(/(.+) (\d+)-(\d+) (.+)/);
                        
                        let scoreStr = '-';
                        let oPts = match.Oleg_pts;
                        let aPts = match.Alex_pts;
                        let oPred = match.Oleg_pred;
                        let aPred = match.Alex_pred;
                        
                        if (matchParts) {
                            const [_, hTeam, hScore, aScore, aTeam] = matchParts;
                            // Если текущая строка - это Home team, пишем H:A, если Away - пишем A:H (чтобы счет был с точки зрения команды в строке)
                            if (hTeam === rowTeam.team) {
                                scoreStr = `${hScore}:${aScore}`;
                            } else {
                                scoreStr = `${aScore}:${hScore}`;
                                // Прогнозы тоже нужно перевернуть, если мы смотрим со стороны гостей? Нет, прогнозы лучше оставить как есть, они привязаны к формату матча
                            }
                        }
                        
                        const getBadgeCls = (pts) => pts >= 4 ? 'win' : (pts > 0 ? 'draw' : 'loss');
                        
                        const ttHtml = `
                            <div class="g-tooltip">
                                <div class="g-tt-match">${match.match}</div>
                                <div>Олег: ${oPred} (<span style="color: ${oPts >= 4 ? '#34a853' : (oPts > 0 ? '#fbbc04' : '#ea4335')}">+${oPts}</span>)</div>
                                <div>Алекс: ${aPred} (<span style="color: ${aPts >= 4 ? '#34a853' : (aPts > 0 ? '#fbbc04' : '#ea4335')}">+${aPts}</span>)</div>
                            </div>
                        `;
                        
                        tdMatrix += `
                            <td class="matrix-col">
                                <div class="matrix-cell">
                                    <div class="matrix-score">${scoreStr}</div>
                                    <div class="matrix-badges">
                                        <div class="m-badge ${getBadgeCls(oPts)}">${oPts}</div>
                                        <div class="m-badge ${getBadgeCls(aPts)}">${aPts}</div>
                                    </div>
                                    ${ttHtml}
                                </div>
                            </td>
                        `;
                    } else {
                        tdMatrix += `<td class="matrix-col"></td>`;
                    }
                }
            });

            rowsHtml += `
                <tr class="${rowClass}">
                    <td class="team-col">
                        <span style="color: #9aa0a6; margin-right: 15px; display: inline-block; width: 15px; text-align: center;">${rowIndex + 1}</span>
                        ${rowTeam.team}
                    </td>
                    ${tdMatrix}
                    <td>${rowTeam.pld}</td>
                    <td>${rowTeam.w}</td>
                    <td>${rowTeam.d}</td>
                    <td>${rowTeam.l}</td>
                    <td>${rowTeam.gd > 0 ? '+'+rowTeam.gd : rowTeam.gd}</td>
                    <td class="pts-col">${rowTeam.pts}</td>
                </tr>
            `;
        });
        
        card.innerHTML = `
            <h3>Group ${groupName}</h3>
            <table class="group-table">
                <thead>
                    <tr>
                        <th class="team-col">Team</th>
                        ${thMatrix}
                        <th>MP</th>
                        <th>W</th>
                        <th>D</th>
                        <th>L</th>
                        <th>GD</th>
                        <th>Pts</th>
                    </tr>
                </thead>
                <tbody>
                    ${rowsHtml}
                </tbody>
            </table>
        `;
        container.appendChild(card);
    }
}

function renderPlayoffs(playoffs) {
    const container = document.getElementById('playoffsContainer');
    if (!container) return;
    
    container.innerHTML = '';
    
    const bracketScroll = document.createElement('div');
    bracketScroll.className = 'bracket-scroll';
    
    // stages in order
    const stageNames = {
        "round_of_32": "1/16 Финала",
        "round_of_16": "1/8 Финала",
        "quarter": "Четвертьфиналы",
        "semi": "Полуфиналы",
        "final": "Финал"
    };
    
    for (const [stageKey, title] of Object.entries(stageNames)) {
        const matches = playoffs[stageKey];
        if (!matches || matches.length === 0) continue;
        
        const stageDiv = document.createElement('div');
        stageDiv.className = 'bracket-stage';
        
        let html = `<div class="b-stage-inner">`;
        html += `<h4 class="stage-title">${title}</h4>`;
        
        matches.forEach(m => {
            const hScore = m.home_score !== null && m.home_score !== '-' ? m.home_score : '';
            const aScore = m.away_score !== null && m.away_score !== '-' ? m.away_score : '';
            
            const isFinished = m.status === 'finished';
            const hWin = isFinished && parseInt(hScore) > parseInt(aScore); // Simplified logic
            const aWin = isFinished && parseInt(aScore) > parseInt(hScore);
            
            // Badges
            let badgesHtml = '';
            if (m.Oleg_pts !== undefined && m.Alex_pts !== undefined) {
                const getBadgeCls = (pts) => pts >= 4 ? 'win' : (pts > 0 ? 'draw' : 'loss');
                badgesHtml = `
                    <div class="b-badges">
                        <div class="m-badge ${getBadgeCls(m.Oleg_pts)}" title="Олег: ${m.Oleg_pred} (+${m.Oleg_pts})">${m.Oleg_pts}</div>
                        <div class="m-badge ${getBadgeCls(m.Alex_pts)}" title="Алекс: ${m.Alex_pred} (+${m.Alex_pts})">${m.Alex_pts}</div>
                    </div>
                `;
            }

            html += `
                <div class="b-match-wrapper">
                    <div class="b-match-card">
                        <div class="b-team ${hWin ? 'winner' : ''}">
                            <span class="b-team-name" title="${m.home}">${m.home}</span>
                            <span class="b-team-score">${hScore}</span>
                        </div>
                        <div class="b-team ${aWin ? 'winner' : ''}">
                            <span class="b-team-name" title="${m.away}">${m.away}</span>
                            <span class="b-team-score">${aScore}</span>
                        </div>
                    </div>
                    ${badgesHtml}
                </div>
            `;
        });
        html += `</div>`;
        stageDiv.innerHTML = html;
        bracketScroll.appendChild(stageDiv);
    }
    
    // Add third place separately? Usually it's floating somewhere, but let's keep it simple.
    
    container.appendChild(bracketScroll);
}


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
    
    // Оставляем только матчи ближайшего игрового дня
    const sorted = [...data.upcoming].sort((a, b) => new Date(a.datetime_utc) - new Date(b.datetime_utc));
    const firstDate = new Date(sorted[0].datetime_utc).toDateString();
    data.upcoming = sorted.filter(m => new Date(m.datetime_utc).toDateString() === firstDate);

    
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

function copyToClipboard(btn) {
    if (!window.DASHBOARD_DATA || !window.DASHBOARD_DATA.upcoming) return;
    
    let text = "Мои прогнозы на завтра:\n\n";
    let hasPredictions = false;
    
    window.DASHBOARD_DATA.upcoming.forEach(match => {
        const score = userPredictions[match.id];
        if (score) {
            hasPredictions = true;
            text += `${match.home || 'TBD'} ${score[0]}:${score[1]} ${match.away || 'TBD'}\n`;
        }
    });
    
    if (!hasPredictions) {
        alert('Нет предстоящих матчей для прогноза.');
        return;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Скопировано!';
        setTimeout(() => {
            btn.innerHTML = originalHTML;
        }, 2000);
    }).catch(err => {
        console.error('Не удалось скопировать', err);
        alert('Не удалось скопировать текст. Попробуйте вручную.');
    });
}
