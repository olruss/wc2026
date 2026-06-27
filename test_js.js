const fs = require('fs');
const dataStr = fs.readFileSync('docs/data.js', 'utf8').replace('window.DASHBOARD_DATA = ', '').replace(/;\n$/, '');
const data = JSON.parse(dataStr);
function renderTeamForm(teamName, teamFormData) {
    if (!teamFormData || !teamFormData[teamName]) return '';
    return teamFormData[teamName].map(match => {
        let dotClass = 'dot-grey';
        if (match.result === 'W') dotClass = 'dot-green';
        else if (match.result === 'D') dotClass = 'dot-yellow';
        else if (match.result === 'L') dotClass = 'dot-red';
        return `<span class="form-dot ${dotClass}" title="${match.score} против ${match.opponent}" style="cursor: help;"></span>`;
    }).join('');
}

const sorted = [...data.upcoming].sort((a, b) => new Date(a.datetime_utc) - new Date(b.datetime_utc));
const now = new Date("2026-06-26T21:50:00-04:00");
const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

let targetDateStr = null;
for (const m of sorted) {
    const mDate = new Date(m.datetime_utc);
    const mDay = new Date(mDate.getFullYear(), mDate.getMonth(), mDate.getDate());
    
    if (mDay > today) {
        targetDateStr = mDate.toDateString();
        break;
    }
}

const upcoming_filtered = sorted.filter(m => new Date(m.datetime_utc).toDateString() === targetDateStr);
console.log("Filtered to date:", targetDateStr, upcoming_filtered.length, "matches");

if (upcoming_filtered.length > 0) {
    const m = upcoming_filtered[0];
    console.log(m.home, "VS", m.away);
    console.log("HOME FORM:", renderTeamForm(m.home, data.team_form));
    console.log("AWAY FORM:", renderTeamForm(m.away, data.team_form));
} else {
    console.log("No upcoming matches found in JS.");
}
