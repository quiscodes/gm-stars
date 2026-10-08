#   GM Stars is a game where the user inputs what NBA team they would want to start a franchise with
#   They are then given a random salary cap for that franchise to build a 5 man roster
#   The user has to create the “best team possible” with that salary given
#   Random constraints are given for each team
#   e.g “team must satisfy all 5 positions” and “pg must shoot > 30% from 3pt line”
#   The roster is then graded based on overall ratings to then receive a final overall score
#   Then the user is lastly prompted if they would like to play again or quit the program


import random


banner = "\n                                                      Welcome to GM Stars!\n" \
"In this interactive NBA game, you will build a franchise and create the best roster possible " \
"based on a random set salary given to you.\nBut hold on... There's a catch! Building this roster " \
"won't be as easy as you think...\nYou will be given random constraints that you must comply to within " \
"the process of creating your team.\nEach roster will be graded by overall ratings at the end. Are you " \
"up for the challenge?\n"


franchises = ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors",
                  "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks",
                  "Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trailblazers", "Utah Jazz", 
                  "Golden State Warriors", "LA Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings", 
                  "Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards", 
                  "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans", "San Antonio Spurs"]


constraints = ["Team must satisfy all 5 positions.", "PG must shoot > 50 percent from FG.", "C must average > 7 rebounds per game."]

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

def display_franchises():
    for team in franchises:
        print(f"\n{team}")

def display_players():
    for player in players:
        print(f"\nPlayer: {player}    Salary: ${players[player]['salary']:,}")

def team_input(user_input):
    user_input = user_input.lower()
    for name in franchises:
        city, team_name = name.rsplit(" ", 1)

        if user_input == name.lower():
            return name
        if user_input == team_name.lower():
            return name
        
    return None

def player_input(user_input):
    user_input = user_input.lower()
    for name in players:
        if user_input == name.lower():
            return name

    return None

def play_game():
    play = input("Would you like to play? (yes/no)\n").lower().strip()
    
    if play == "yes":
        display_franchises()
        team = input("\nPlease select your franchise.\n")
        franchise = team_input(team)

        while franchise is None:
            print("Franchise not found. Please try again.")
            team = input("Please select your franchise.\n")
            franchise = team_input(team)

        salary_cap = random.randrange(100_000_000, 215_000_000, 5_000_000)
        remaining_salary = salary_cap

        display_players()
        print (f"\nYour salary cap is ${salary_cap:,}.")
        print("\nBuild your 5-man roster!")
        print("\nYour constraint is:" , constraints[0])

        roster = []

        for i in range(1, 6):
            while True:
                p = input(f"\nPlayer {i}. ")
                player = player_input(p)

                if player is None:
                    print("Player not found. Please try again.")
                    continue

                if player in roster:
                    print(f"{player} is already on your roster. Please try again with a new player.\n")
                    continue

                if players[player]['salary'] > remaining_salary:
                    print(f"You do not have enough money to draft this player! This player costs ${players[player]['salary']:,}. Please try again.\n")
                    continue

                break

            roster.append(player)
            remaining_salary -= players[player]['salary']
            print(f"\nYour remaining salary is ${remaining_salary:,}.\n")
            
        print(f"Your completed 5-man roster:\n1. {roster[0]}\n2. {roster[1]}\n3. {roster[2]}\n4. {roster[3]}\n5. {roster[4]}\n")
        passed = check_roster(roster)

        overall = grade_roster(roster)

        if passed:
            print("Your roster has passed the constraint check!\n")
            print(f"Team Overall Rating: {overall}")
            print(team_label(overall))

        else:
            print("You have failed to create a roster that passes the constraint check!\n")
            print("Team Overall Rating: 0")
            print(f"Expected Overall: {overall}")

        play = input("\nWould you like to play again? (yes/no)\n").lower().strip()
        if play == "yes":
            play_game()
    
    else:
        print("Thanks for checking out the game. Maybe next time!")

def check_roster(roster):
    positions = []
    for player in roster:
        positions.append(players[player]['position'])

    required_positions = {'PG', 'SG', 'SF', 'PF', 'C'}

    return set(positions) == required_positions

def grade_roster(roster):
    pra_values = []

    for player in players:
        pra = (players[player]['ppg'] + players[player]['rebounds'] + players[player]['assists'])

        pra_values.append(pra)

    pra_values.sort()

    floor = sum(pra_values[:5])
    ceiling = sum(pra_values[-5:])

    team_pra = 0

    for player in roster:
        team_pra += players[player]['ppg'] + players[player]['rebounds'] + players[player]['assists']
    
    overall = 60 + (team_pra - floor) / (ceiling - floor) * 39
    overall = max(60, min(99, overall))
    overall = round(overall)

    return overall

def team_label(overall):
    if overall >= 95:
        return "Super Team"

    elif overall >= 90:
        return "Contenders"

    elif overall >= 85:
        return "Playoff Team"

    elif overall >= 80:
        return "Play-In Team"

    elif overall >= 70:
        return "Maybe next year!"

    else:
        return "Needs Rebuild"

def main():
    print(banner)
    play_game()

main()