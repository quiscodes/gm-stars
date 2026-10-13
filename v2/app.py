# =============================================================================
# GM STARS v2 — app.py  (the Flask "backend")
# =============================================================================
#
#   - Defines the web routes (URLs) of the game: /, /start, /draft, /results, /new-game
#   - Holds the game rules: salary cap, pick validation, constraint check, grading
#   - Stores each player's in-progress game in Flask's `session` (a signed cookie)
#   - Hands data to templates/index.html, which turns it into the page you see
#
# The flow of one game:
#   /          home page: choose a franchise
#   /start     (POST) validates the franchise, rolls a random cap, starts the game
#   /draft     pick players one at a time until the roster is full
#   /results   check the constraint, grade the roster, show the final score
#   /new-game  wipe the session and go back home
#
# Original v1:
#   Command-line project: The user picks an NBA franchise, gets a random salary cap, and drafts a
#   5-man roster that must satisfy a constraint. The roster is graded 60-99 overall.
#
# Planned for later versions:
#   v2.2 real NBA data/APIs   v2.3 difficulty system   v2.4 accounts
#   v2.5 leaderboards         v2.6 images/animations
# =============================================================================

import os
import random

from flask import Flask, redirect, render_template, request, session, url_for

from game_data import constraints, franchises, players

from operator import itemgetter

# -----------------------------------------------------------------------------
# SETTINGS
# -----------------------------------------------------------------------------
# Game rules live here as named constants so you never have to hunt for a
# "magic number" buried inside a function.

ROSTER_SIZE = 5
REQUIRED_POSITIONS = {"PG", "SG", "SF", "PF", "C"}

# PRA benchmarks for the roster rating. These stay fixed as the player pool grows:
# a 146-PRA roster rates about 85, and a 226-PRA roster rates about 99.
PRA_FOR_85 = 146
PRA_FOR_99 = 226

CAP_MIN = 100_000_000
CAP_MAX = 215_000_000
CAP_STEP = 5_000_000

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "local-dev-key")

# -----------------------------------------------------------------------------
# TEMPLATE DATA
# -----------------------------------------------------------------------------

@app.context_processor
def shared_template_data():
    """Make these values available in index.html without passing them each time."""
    return {
        "franchises": franchises,
        "players": players,
        "roster_size": ROSTER_SIZE,
    }

# -----------------------------------------------------------------------------
# INPUT LOOKUPS
# -----------------------------------------------------------------------------
# These bring back v1's friendly matching: case-insensitive, extra spaces
# ignored, and franchises accept either the full name or the nickname.
# Each returns the official spelling from game_data, or None if nothing matches.

def find_franchise(user_input):
    """'celtics' or 'Boston Celtics' -> 'Boston Celtics'."""
    text = user_input.strip().lower()
    for name in franchises:
        nickname = name.rsplit(" ", 1)[1]
        if text in (name.lower(), nickname.lower()):
            return name
    return None

def find_player(user_input):
    """'lebron james' -> 'LeBron James'."""
    text = user_input.strip().lower()
    for name in players:
        if text == name.lower():
            return name
    return None

# -----------------------------------------------------------------------------
# GAME LOGIC (no Flask in here — these are plain functions, easy to test)
# -----------------------------------------------------------------------------

def player_choices():
    """Players who are not drafted yet AND still fit under the remaining cap."""
    roster = session.get("roster", [])
    remaining = session.get("remaining_salary", 0)
    available = [
        {"name": name, **details}
        for name, details in players.items()
        if name not in roster and details['salary'] <= remaining]
    
    return sorted(available, key=itemgetter("salary"), reverse=True)

def player_pra(name):
    """Points + rebounds + assists for one player."""
    stats = players[name]
    return stats["ppg"] + stats["rebounds"] + stats["assists"]

def check_roster(roster):
    """Constraint #1: the roster must cover all five positions."""
    return {players[name]["position"] for name in roster} == REQUIRED_POSITIONS

def grade_roster(roster):
    """Map team PRA to an overall rating using fixed 85 and 99 benchmarks."""
    team_pra = sum(player_pra(name) for name in roster)
    overall = 85 + (team_pra - PRA_FOR_85) / (PRA_FOR_99 - PRA_FOR_85) * 14
    return round(max(60, min(99, overall)))

def team_label(overall):
    """Turn the 60-99 number into a title."""
    if overall >= 95:
        return "Super Team"
    if overall >= 90:
        return "Contenders"
    if overall >= 80:
        return "Playoff Team"
    if overall >= 75:
        return "Play-In Team"
    if overall >= 70:
        return "Rebuilding Team"
    return "Tanking For #1 Pick?"

# -----------------------------------------------------------------------------
# ROUTES
# -----------------------------------------------------------------------------

@app.route("/")
def home():
    """Home page: pick a franchise."""
    return render_template("index.html", stage="home")

@app.post("/start")
def start_game():
    """Validate the franchise, roll a random salary cap, begin a new game."""
    franchise = find_franchise(request.form.get("franchise", ""))
    if franchise is None:
        return render_template("index.html", stage="home", error="Choose a franchise from the list.")

    # +CAP_STEP because randrange excludes its upper bound; this lets $215M happen.
    cap = random.randrange(CAP_MIN, CAP_MAX + CAP_STEP, CAP_STEP)

    session.clear()
    session.update(franchise=franchise, salary_cap=cap, remaining_salary=cap, roster=[])
    return redirect(url_for("draft"))

@app.route("/draft", methods=["GET", "POST"])
def draft():
    """GET shows the draft page. POST tries to draft one player."""
    if "salary_cap" not in session:
        return redirect(url_for("home"))

    roster = session["roster"]

    # Roster already full (e.g. user pressed Back): go to results instead of
    # letting a 6th player be added.
    if len(roster) >= ROSTER_SIZE:
        return redirect(url_for("results"))

    error = None
    if request.method == "POST":
        name = find_player(request.form.get("player", ""))

        # One validation chain, same checks as v1: exists -> not drafted -> affordable.
        if name is None:
            error = "Choose a player from the list."
        elif name in roster:
            error = f"{name} is already on your roster."
        elif players[name]["salary"] > session["remaining_salary"]:
            error = "You do not have enough salary for that player."
        else:
            roster.append(name)
            session["roster"] = roster
            session["remaining_salary"] -= players[name]["salary"]

            # Post/Redirect/Get: after a successful pick, redirect to a fresh GET.
            # Without this, refreshing the page re-submits the form and re-sends
            # the same pick. If the roster just became full, /draft redirects on
            # to /results above.
            return redirect(url_for("draft"))

    return render_template(
        "index.html",
        stage="draft",
        franchise=session["franchise"],
        salary_cap=session["salary_cap"],
        remaining_salary=session["remaining_salary"],
        roster=roster,
        choices=player_choices(),
        constraint=constraints[0],
        error=error,
    )

@app.route("/results")
def results():
    """Check the constraint, grade the roster, show the final screen."""
    roster = session.get("roster", [])
    if len(roster) != ROSTER_SIZE:
        return redirect(url_for("draft"))

    passed = check_roster(roster)
    overall = grade_roster(roster)
    return render_template(
        "index.html",
        stage="results",
        franchise=session["franchise"],
        roster=[{"name": name, **players[name]} for name in roster],
        passed=passed,
        overall=overall,
        label=team_label(overall),
    )

@app.route("/new-game")
def new_game():
    """Abandon the current game and return home."""
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
