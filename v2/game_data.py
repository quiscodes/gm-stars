"""Original hardcoded V1 game data, carried into the Flask version."""

from operator import itemgetter
import csv
from pathlib import Path

franchises = ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors",
                  "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks",
                  "Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trailblazers", "Utah Jazz", 
                  "Golden State Warriors", "LA Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings", 
                  "Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards", 
                  "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans", "San Antonio Spurs"]



constraints = ['Team must satisfy all 5 positions.', 'PG must shoot > 50 percent from FG.', 'C must average > 7 rebounds per game.']

players = {
    "Nikola Jokic": {"position": "C", "salary": 55_224_526, "ppg": 27.7, "rebounds": 12.9, "assists": 10.7, "fg_pct": .569},
    "Luka Doncic": {"position": "PG", "salary": 45_999_660, "ppg": 33.5, "rebounds": 7.7, "assists": 8.3, "fg_pct": .476},
    "Shai Gilgeous-Alexander": {"position": "PG", "salary": 38_333_050, "ppg": 31.1, "rebounds": 4.3, "assists": 6.6, "fg_pct": .553},
    "Giannis Antetokounmpo": {"position": "PF", "salary": 54_126_450, "ppg": 27.6, "rebounds": 9.8, "assists": 5.4, "fg_pct": .624},
    "Victor Wembanyama": {"position": "C", "salary": 13_376_880, "ppg": 25.0, "rebounds": 11.5, "assists": 3.1, "fg_pct": .512},
    "Tyrese Maxey": {"position": "PG", "salary": 37_958_760, "ppg": 28.3, "rebounds": 4.1, "assists": 6.6, "fg_pct": .462},
    "Jalen Johnson": {"position": "SF", "salary": 30_000_000, "ppg": 22.5, "rebounds": 10.3, "assists": 7.9, "fg_pct": .489},
    "Cade Cunningham": {"position": "PG", "salary": 46_394_100, "ppg": 23.9, "rebounds": 5.5, "assists": 9.9, "fg_pct": .461},
    "Kawhi Leonard": {"position": "SF", "salary": 50_000_000, "ppg": 27.9, "rebounds": 6.4, "assists": 3.6, "fg_pct": .505},
    "Jaylen Brown": {"position": "SF", "salary": 53_142_264, "ppg": 28.7, "rebounds": 6.9, "assists": 5.1, "fg_pct": .477},
    "Donovan Mitchell": {"position": "SG", "salary": 46_394_100, "ppg": 27.9, "rebounds": 4.5, "assists": 5.7, "fg_pct": .483},
    "Joel Embiid": {"position": "C", "salary": 55_224_526, "ppg": 26.9, "rebounds": 7.7, "assists": 3.9, "fg_pct": .489},
    "Jamal Murray": {"position": "PG", "salary": 46_394_100, "ppg": 25.4, "rebounds": 4.4, "assists": 7.1, "fg_pct": .483},
    "Anthony Edwards": {"position": "SG", "salary": 45_550_512, "ppg": 28.8, "rebounds": 5.0, "assists": 3.7, "fg_pct": .489},
    "Kevin Durant": {"position": "SF", "salary": 54_708_609, "ppg": 26.0, "rebounds": 5.5, "assists": 4.8, "fg_pct": .520},
    "Deni Avdija": {"position": "SF", "salary": 14_375_000, "ppg": 24.2, "rebounds": 6.9, "assists": 6.7, "fg_pct": .462},
    "James Harden": {"position": "SG", "salary": 39_446_090, "ppg": 23.6, "rebounds": 8.0, "assists": 8.1, "fg_pct": .434},
    "Jalen Brunson": {"position": "PG", "salary": 34_944_001, "ppg": 26.0, "rebounds": 3.3, "assists": 6.8, "fg_pct": .467},
    "Lauri Markkanen": {"position": "PF", "salary": 46_394_100, "ppg": 26.7, "rebounds": 6.9, "assists": 2.1, "fg_pct": .477},
    "Alperen Sengun": {"position": "C", "salary": 33_944_954, "ppg": 20.4, "rebounds": 8.9, "assists": 6.2, "fg_pct": .519},
    "Stephen Curry": {"position": "PG", "salary": 59_606_817, "ppg": 26.6, "rebounds": 3.6, "assists": 4.7, "fg_pct": .468},
    "Jayson Tatum": {"position": "PF", "salary": 54_126_450, "ppg": 21.8, "rebounds": 5.3, "assists": 2.9, "fg_pct": .411},
    "Devin Booker": {"position": "SG", "salary": 53_142_264, "ppg": 26.1, "rebounds": 3.9, "assists": 6.0, "fg_pct": .456},
    "LeBron James": {"position": "PF", "salary": 52_627_153, "ppg": 20.9, "rebounds": 6.1, "assists": 7.2, "fg_pct": .515},
    "Anthony Davis": {"position": "C", "salary": 54_126_450, "ppg": 20.4, "rebounds": 11.1, "assists": 2.8, "fg_pct": .506},
    "Karl-Anthony Towns": {"position": "C", "salary": 53_142_264, "ppg": 20.1, "rebounds": 11.9, "assists": 3.0, "fg_pct": .501},
    "Austin Reaves": {"position": "SG", "salary": 13_937_574, "ppg": 23.3, "rebounds": 4.7, "assists": 5.5, "fg_pct": .490},
    "Josh Giddey": {"position": "SG", "salary": 25_000_000, "ppg": 17.0, "rebounds": 8.3, "assists": 9.1, "fg_pct": .448},
    "Paolo Banchero": {"position": "PF", "salary": 15_334_769, "ppg": 22.2, "rebounds": 8.4, "assists": 5.2, "fg_pct": .459},
    "Michael Porter Jr": {"position": "SF", "salary": 38_333_050, "ppg": 24.2, "rebounds": 7.1, "assists": 3.0, "fg_pct": .463},
    "Pascal Siakam": {"position": "PF", "salary": 45_550_512, "ppg": 24.0, "rebounds": 6.6, "assists": 3.8, "fg_pct": .484},
    "Keyonte George": {"position": "PG", "salary": 4_278_960, "ppg": 23.6, "rebounds": 3.7, "assists": 6.1, "fg_pct": .456},
    "Scottie Barnes": {"position": "PF", "salary": 38_661_750, "ppg": 18.1, "rebounds": 7.5, "assists": 5.9, "fg_pct": .507},
    "Jalen Duren": {"position": "C", "salary": 6_483_144, "ppg": 19.5, "rebounds": 10.5, "assists": 2.8, "fg_pct": .650},
    "Amen Thompson": {"position": "PG", "salary": 9_690_000, "ppg": 18.3, "rebounds": 7.8, "assists": 5.3, "fg_pct": .534},
    "Cooper Flagg": {"position": "SF", "salary": 13_825_920, "ppg": 21.0, "rebounds": 6.7, "assists": 4.5, "fg_pct": .468},
    "Bam Adebayo": {"position": "C", "salary": 37_096_620, "ppg": 20.1, "rebounds": 10.0, "assists": 3.2, "fg_pct": .442},
    "Julius Randle": {"position": "PF", "salary": 30_864_198, "ppg": 21.1, "rebounds": 6.7, "assists": 5.0, "fg_pct": .481},
    "Evan Mobley": {"position": "PF", "salary": 46_394_100, "ppg": 18.2, "rebounds": 9.0, "assists": 3.6, "fg_pct": .606},
    "Trey Murphy III": {"position": "SF", "salary": 25_000_000, "ppg": 21.5, "rebounds": 5.7, "assists": 3.8, "fg_pct": .470},
    "Jimmy Butler": {"position": "SF", "salary": 54_126_450, "ppg": 20.0, "rebounds": 5.6, "assists": 4.9, "fg_pct": .519},
    "LaMelo Ball": {"position": "PG", "salary": 37_958_760, "ppg": 20.1, "rebounds": 4.8, "assists": 7.1, "fg_pct": .407},
    "Kevin Porter Jr": {"position": "PG", "salary": 5_134_000, "ppg": 17.4, "rebounds": 5.2, "assists": 7.4, "fg_pct": .465},
    "Walker Kessler": {"position": "C", "salary": 4_878_930, "ppg": 14.4, "rebounds": 10.8, "assists": 3.0, "fg_pct": .703},
    "Zion Williamson": {"position": "PF", "salary": 39_446_090, "ppg": 21.0, "rebounds": 5.7, "assists": 3.2, "fg_pct": .600},
    "Brandon Ingram": {"position": "SF", "salary": 38_095_238, "ppg": 21.5, "rebounds": 5.6, "assists": 3.7, "fg_pct": .477},
    "Domantas Sabonis": {"position": "C", "salary": 42_336_000, "ppg": 15.8, "rebounds": 11.4, "assists": 4.1, "fg_pct": .543},
    "Tyler Herro": {"position": "SG", "salary": 31_000_000, "ppg": 20.5, "rebounds": 4.8, "assists": 4.8, "fg_pct": .480},
    "Chet Holmgren": {"position": "C", "salary": 13_731_368, "ppg": 17.1, "rebounds": 8.9, "assists": 1.7, "fg_pct": .557},
    "Ja Morant": {"position": "PG", "salary": 39_446_090, "ppg": 19.5, "rebounds": 3.3, "assists": 8.1, "fg_pct": .410},
}

def load_csv_players():
    """Apply CSV profiles/salaries to V1 players and load complete new players.

    Existing V1 stats act as fallbacks while the larger CSV is being filled in.
    A brand-new player is added only after all game-required stats are present.
    """
    import re
    import unicodedata

    csv_path = Path(__file__).with_name("player_data.csv")
    if not csv_path.exists():
        return {}

    csv_players = {}
    stat_fields = ("ppg", "rebounds", "assists", "fg_pct")
    required_fields = ("position", "salary", *stat_fields)
    optional_stat_fields = ("three_pt_pct", "steals", "blocks", "turnovers")

    def name_key(value):
        normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
        return re.sub(r"[^a-z0-9]", "", normalized.casefold())

    existing_names = {name_key(name): name for name in players}

    with csv_path.open(newline="", encoding="utf-8-sig") as data_file:
        for row in csv.DictReader(data_file):
            source_name = (row.get("name") or "").strip()
            if not source_name:
                continue

            name = existing_names.get(name_key(source_name), source_name)
            details = dict(players.get(name, {}))
            try:
                team = (row.get("team") or "").strip()
                position = (row.get("position") or "").strip().upper()
                salary = (row.get("salary") or "").replace("_", "").replace(",", "").replace("$", "").strip()

                if team:
                    details["team"] = team
                if position:
                    details["position"] = position.split("/")[0].strip()
                if salary:
                    details["salary"] = int(salary)
                for field in (*stat_fields, *optional_stat_fields):
                    value = (row.get(field) or "").strip()
                    if value:
                        details[field] = float(value)

                if not all(field in details for field in required_fields):
                    continue
                csv_players[name] = details
            except (TypeError, ValueError):
                continue

    return csv_players


players.update(load_csv_players())


player_dicts = list(players.values())
sorted_players = sorted(player_dicts, key=itemgetter('salary'), reverse=True)

split_franchises = [team.rsplit(" ", 1) for team in franchises]
sorted_split = sorted(split_franchises, key=itemgetter(1))
franchises = [" ".join(team) for team in sorted_split]
