# World Cup Betting Tracker - Project Context

This project is a lightweight, local-first system for tracking World Cup match predictions and calculating scores.

## Architecture & Data Storage
- **Data Format**: All tracking happens locally using `csv` or `json` files in the `data/` folder.
- **External Services**: **NO API keys or paid sources can be used.** Do not propose or use paid APIs.
- **Data Sourcing**: Fixtures, results, and tournament tables must be retrieved by crafting scripts that pull/scrape data from free, public web pages, or by performing standard web searches for match results.
- **Execution**: Computing standings is done via a simple local python script `compute.py`.
- **Language**: All communication with the user must be in Russian.

## Core Workflows

### 1. Making Predictions (Делать прогнозы)
- The agent should analyze the `analytics/` folder (which contains team-specific knowledge), past match results in `data/fixtures.json`, and general football knowledge.
- For upcoming `scheduled` matches (grouped by day or matchday), the agent generates a proposed set of predictions (expected scores, e.g., 2-1) for the user (Oleg).
- Optionally, the agent updates `data/upcoming_ai.json` with short analytical summaries and suggested scores.

### 2. Locking Bets (Фиксировать ставки)
- The user (Oleg) will review, approve, or correct the agent's proposed predictions.
- Once Oleg's predictions are finalized, the user will manually provide Alex's predictions.
- The agent must then open `data/predictions.json` and insert/update the exact scoreline arrays for both "Oleg" and "Alex" for the corresponding match IDs (e.g., `"I5": [1, 2]`).

### 3. Finding and Updating Match Results & Brackets
- **Search**: Use the `search_web` tool to find the real-world results of the concluded matches for the specific date. Ensure you match the correct teams.
- **Update Results**: Open `data/fixtures.json` and change the `"status"` of the concluded match from `"scheduled"` to `"finished"`. Update `"home_score"` and `"away_score"` with the actual goals scored.
- **Scoring**: Run `python3 compute.py` to calculate updated prediction points.
  - *Scoring Rules (Max 6 points)*: 3 points for correct match result (W/D/L), 1 point for exact Home goals, 1 point for exact Away goals, 1 point for exact goal difference.
- **Tournament Bracket**: As the group stage ends, scripts should determine group winners/runners-up and update the placeholder names (e.g., "Winner Group A") in `data/fixtures.json` for playoff stages (`R32`, `R16`, `QF`, etc.).

### 4. Updating and Deploying the UI
- **Architecture**: The project includes a web-based dashboard hosted on GitHub Pages (static site, no backend). Frontend code (`index.html`, `style.css`, `app.js`) is in the `docs/` folder.
- **Data Integration**: Running `python3 compute.py` automatically regenerates `docs/data.js` (which assigns stats to `window.DASHBOARD_DATA`) and busts the cache by appending `?v=timestamp` to asset links in `docs/index.html`.
- **Deployment**:
  1. Make sure `python3 compute.py` has been run.
  2. Commit and push changes: `git add .`, `git commit -m "Update match results / UI tweaks"`, `git push origin main`.
  3. GitHub Pages deploys automatically from the `/docs` folder on the `main` branch. The live site at `https://olruss.github.io/wc2026/` updates within 1-2 minutes.
- **Important**: When changing UI layout, modify `docs/index.html` and `docs/style.css`, test locally via Python scripts or local server, and then push.

## Guidelines for Output
- Format match results and standings so they are perfectly readable when copied and pasted into Telegram. Avoid ASCII box-drawing characters (`┌─┬`).
- Use a clean plain-text list format without emojis.
- Always translate player names to Russian (e.g., Олег, Алекс).
- Always include a short, engaging analytical commentary comparing the predictions (addressed to both players as a group, using third-person references to their names: "Олег поставил...", "Алекс угадал...").
