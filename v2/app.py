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
#   v2.2 real NBA data   v2.3 difficulty system   v2.4 accounts
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


ROSTER_SIZE = 5
REQUIRED_POSITIONS = {"PG", "SG", "SF", "PF", "C"}

# Team PRA totals mapped to overall grades. The curve rewards strong rosters
# while leaving room for both low 60s and 99 overall teams.
PRA_GRADE_ANCHORS = (
    (40, 60),
    (70, 65),
    (90, 72),
    (110, 82),
    (130, 90),
    (150, 95),
    (175, 99),
)

CAP_STEP = 5_000_000
DIFFICULTIES = {
    "easy": {"label": "Easy", "minimum": 150_000_000, "maximum": 200_000_000},
    "hard": {"label": "Hard", "minimum": 100_000_000, "maximum": 150_000_000},
    "impossible": {"label": "Impossible", "minimum": 50_000_000, "maximum": 100_000_000},
}
POSITIONS = ("PG", "SG", "SF", "PF", "C")
TEAM_NAMES = {
    "ATL": "Atlanta", "BOS": "Boston", "BKN": "Brooklyn", "CHA": "Charlotte",
    "CHI": "Chicago", "CLE": "Cleveland", "DAL": "Dallas", "DEN": "Denver",
    "DET": "Detroit", "GSW": "Golden State", "HOU": "Houston", "IND": "Indiana",
    "LAC": "LA Clippers", "LAL": "LA Lakers", "MEM": "Memphis", "MIA": "Miami",
    "MIL": "Milwaukee", "MIN": "Minnesota", "NOP": "New Orleans", "NYK": "New York",
    "OKC": "Oklahoma City", "ORL": "Orlando", "PHI": "Philadelphia", "PHX": "Phoenix",
    "POR": "Portland", "SAC": "Sacramento", "SAS": "San Antonio", "TOR": "Toronto",
    "UTA": "Utah", "WAS": "Washington",
}

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
# GAME LOGIC
# -----------------------------------------------------------------------------

def player_choices():
    """Undrafted, affordable players who satisfy any position/team slots."""
    roster = session.get("roster", [])
    remaining = session.get("remaining_salary", 0)
    filled_positions = {players[name]["position"] for name in roster}
    assignments = session.get("position_teams", {})
    available = [
        {"name": name, **details}
        for name, details in players.items()
        if name not in roster
        and details["salary"] <= remaining
        and details["position"] not in filled_positions
        and details["position"] in REQUIRED_POSITIONS
        and (not assignments or details.get("team") == assignments.get(details["position"]))
    ]
    return sorted(available, key=itemgetter("salary"), reverse=True)

def player_pra(name):
    """Points + rebounds + assists for one player."""
    stats = players[name]
    return stats["ppg"] + stats["rebounds"] + stats["assists"]

def challenge_pass(rule, roster, assignments=None):
    """Evaluate one selected challenge against a five-player roster."""
    details = [players[name] for name in roster]
    by_position = {item["position"]: item for item in details}
    teams = [item.get("team", "") for item in details]
    assignments = assignments or {}

    if rule == "Team must satisfy all 5 positions.":
        return set(by_position) == REQUIRED_POSITIONS
    if rule.startswith("For each position, draft"):
        return all(by_position.get(pos, {}).get("team") == team for pos, team in assignments.items())
    if rule.startswith("The ") and " must play for the " in rule:
        position = rule.split("The ", 1)[1].split(" must play", 1)[0]
        team = rule.rsplit("the ", 1)[1].rstrip(".")
        return by_position.get(position, {}).get("team") == team
    if rule.startswith("All five players must play for the "):
        team = rule.rsplit("the ", 1)[1].rstrip(".")
        return all(value == team for value in teams)
    if rule.startswith("At least two players must play for the "):
        team = rule.rsplit("the ", 1)[1].rstrip(".")
        return teams.count(team) >= 2
    if rule == "No more than two players may play for the same team.":
        return max((teams.count(team) for team in set(teams)), default=0) <= 2
    if rule.startswith("At least three players must shoot"):
        return sum(item.get("three_pt_pct", 0) >= .35 for item in details) >= 3
    if rule.startswith("The team average 3-point percentage"):
        threshold = .40 if "40%" in rule else .38
        return sum(item.get("three_pt_pct", 0) for item in details) / len(details) >= threshold
    if rule.startswith("At least three players must shoot 45%"):
        return sum(item.get("fg_pct", 0) >= .45 for item in details) >= 3
    if rule.startswith("The team average field-goal percentage"):
        return sum(item.get("fg_pct", 0) for item in details) / len(details) >= .47
    if rule.startswith("At least two players must average 20"):
        return sum(item.get("ppg", 0) >= 20 for item in details) >= 2
    if rule.startswith("At least one player must average 25"):
        return any(item.get("ppg", 0) >= 25 for item in details)
    if rule.startswith("At least two players must each average 25 or more PRA"):
        return sum(item.get("ppg", 0) + item.get("rebounds", 0) + item.get("assists", 0) >= 25 for item in details) >= 2
    if rule.startswith("The point guard must"):
        return by_position.get("PG", {}).get("assists", 0) >= 5
    if rule.startswith("The team must combine for at least 15 assists"):
        return sum(item.get("assists", 0) for item in details) >= 15
    if rule.startswith("The center must average at least 8 rebounds"):
        return by_position.get("C", {}).get("rebounds", 0) >= 8
    if rule.startswith("The center must average at least 10 rebounds"):
        return by_position.get("C", {}).get("rebounds", 0) >= 10
    if rule.startswith("The power forward and center"):
        return by_position.get("PF", {}).get("rebounds", 0) + by_position.get("C", {}).get("rebounds", 0) >= 15
    if rule.startswith("The team must combine for at least 5 steals"):
        return sum(item.get("steals", 0) + item.get("blocks", 0) for item in details) >= 5
    if rule.startswith("At least two players must average 1 or more steals"):
        return sum(item.get("steals", 0) >= 1 for item in details) >= 2
    if rule.startswith("The center must average at least 1 block"):
        return by_position.get("C", {}).get("blocks", 0) >= 1
    if rule.startswith("The team must average no more than 7 turnovers"):
        return sum(item.get("turnovers", 0) for item in details) <= 7
    if rule.startswith("At least three players must average fewer than 2 turnovers"):
        return sum(item.get("turnovers", 0) < 2 for item in details) >= 3
    if rule.startswith("At least two players must have a salary of $30 million or less"):
        return sum(item.get("salary", 0) <= 30_000_000 for item in details) >= 2
    if rule.startswith("No more than one player may have a salary above $35 million"):
        return sum(item.get("salary", 0) > 35_000_000 for item in details) <= 1
    return False


def check_roster(roster):
    """All mode challenges must pass; every mode includes position coverage."""
    if not challenge_pass("Team must satisfy all 5 positions.", roster):
        return False
    assignments = session.get("position_teams", {})
    if assignments and not challenge_pass("For each position, draft a player from its assigned team.", roster, assignments):
        return False
    return all(challenge_pass(rule, roster, assignments) for rule in session.get("challenges", []))


def find_affordable_roster(cap, assignments=None):
    """Find an example five-position roster that fits a cap and assignments."""
    candidates = {}
    for position in POSITIONS:
        candidates[position] = [
            name for name, details in players.items()
            if details.get("position") == position
            and details.get("salary", cap + 1) <= cap
            and (not assignments or details.get("team") == assignments.get(position))
        ]
        random.shuffle(candidates[position])
        if not candidates[position]:
            return None

    # Try random affordable combinations, favoring low-salary candidates so
    # the tightest cap can still produce a playable game.
    for _ in range(500):
        lineup = []
        used_salary = 0
        for position in POSITIONS:
            choices = sorted(candidates[position], key=lambda name: players[name]["salary"])
            pool = choices[:max(1, min(15, len(choices)))]
            affordable = [name for name in pool if used_salary + players[name]["salary"] <= cap]
            if not affordable:
                break
            choice = random.choice(affordable)
            lineup.append(choice)
            used_salary += players[choice]["salary"]
        if len(lineup) == ROSTER_SIZE:
            return lineup
    return None


def choose_game_challenges(difficulty, cap):
    """Create challenges and a feasible team assignment for a new game."""
    extra_rules = [rule for rule in constraints if rule != constraints[0]
                   and "{position_team_assignments}" not in rule
                   and "{position}" not in rule and "{team}" not in rule]

    if difficulty == "hard":
        # Try random NBA teams for each position until the salary range has
        # at least one possible starting five.
        for _ in range(250):
            eligible = {
                pos: sorted({data.get("team") for data in players.values()
                             if data.get("position") == pos and data.get("team")})
                for pos in POSITIONS
            }
            assignments = {pos: random.choice(eligible[pos]) for pos in POSITIONS}
            witness = find_affordable_roster(cap, assignments)
            if witness:
                viable_rules = [rule for rule in extra_rules
                                if challenge_pass(rule, witness, assignments)]
                if viable_rules:
                    return assignments, [random.choice(viable_rules)]
        # The team mapping itself is randomly generated; fall back to a valid
        # lineup's teams if a very low cap has too few random combinations.
        witness = find_affordable_roster(cap)
        if witness:
            assignments = {players[name]["position"]: players[name].get("team") for name in witness}
            viable_rules = [rule for rule in extra_rules if challenge_pass(rule, witness, assignments)]
            return assignments, [random.choice(viable_rules)] if viable_rules else []
        return {}, []

    if difficulty == "impossible":
        for _ in range(80):
            witness = find_affordable_roster(cap)
            if witness:
                viable_rules = [rule for rule in extra_rules if challenge_pass(rule, witness)]
                if len(viable_rules) >= 2:
                    return {}, random.sample(viable_rules, 2)
        return {}, []

    return {}, []

def grade_roster(roster):
    """Grade the five-player roster from its combined points, rebounds, and assists."""
    team_pra = sum(player_pra(name) for name in roster)

    for (lower_pra, lower_grade), (upper_pra, upper_grade) in zip(
        PRA_GRADE_ANCHORS,
        PRA_GRADE_ANCHORS[1:],
    ):
        if team_pra <= upper_pra:
            progress = (team_pra - lower_pra) / (upper_pra - lower_pra)
            grade = lower_grade + progress * (upper_grade - lower_grade)
            return round(max(60, min(99, grade)))

    return 99

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
    """Validate the franchise and difficulty, then begin a new game."""
    franchise = find_franchise(request.form.get("franchise", ""))
    if franchise is None:
        return render_template("index.html", stage="home", error="Choose a franchise from the list.")

    difficulty = request.form.get("difficulty", "easy").lower()
    if difficulty not in DIFFICULTIES:
        difficulty = "easy"
    settings = DIFFICULTIES[difficulty]
    cap = random.randrange(settings["minimum"], settings["maximum"] + CAP_STEP, CAP_STEP)
    assignments, challenges = choose_game_challenges(difficulty, cap)
    if not find_affordable_roster(cap, assignments):
        # Keep a new game playable if the supplied data changes later.
        assignments, challenges = {}, []
        cap = 100_000_000

    session.clear()
    session.update(franchise=franchise, difficulty=difficulty, salary_cap=cap,
                   remaining_salary=cap, roster=[], position_teams=assignments,
                   challenges=challenges)
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
        picked_positions = {players[picked]["position"] for picked in roster}
        position = players[name]["position"] if name else None
        assigned_team = session.get("position_teams", {}).get(position)

        if name is None:
            error = "Choose a player from the list."
        elif name in roster:
            error = f"{name} is already on your roster."
        elif position not in REQUIRED_POSITIONS or position in picked_positions:
            error = "Choose a player for an open position."
        elif assigned_team and players[name].get("team") != assigned_team:
            error = "Choose a player from the team assigned to that position."
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
        difficulty=DIFFICULTIES[session.get("difficulty", "easy")]["label"],
        salary_cap=session["salary_cap"],
        remaining_salary=session["remaining_salary"],
        roster=roster,
        choices=player_choices(),
        challenges=([
            "Draft one player at each position from their assigned team: " + ", ".join(
                f"{position} → {TEAM_NAMES.get(team, team)}" for position, team in session.get("position_teams", {}).items()
            )
        ] if session.get("position_teams") else []) + session.get("challenges", []),
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
        difficulty=DIFFICULTIES[session.get("difficulty", "easy")]["label"],
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
