#   GM Stars is a game where the user inputs what NBA team they would want to start a franchise with
#   They are then given a random salary cap for that franchise to build a 5 man roster
#   The user has to create the “best team possible” with that salary given
#   Random constraints are given for each team
#   e.g “team must satisfy all 5 positions” and “pg must shoot > 30% from 3pt line”
#   The roster is then graded based on overall ratings to then receive a final overall score
#   Then the user is lastly prompted if they would like to play again or quit the program
#


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

salary_cap = random.randint(150_000_000, 250_000_000)

constraints = ["Team must satisfy all 5 positions.", "PG must shoot > 30% from 3.", "C must average > 7 rebounds per game."]

players = {
    # PG
    "Luka Doncic":          {"position": "PG", "salary": 43_800_000, "ppg": 32.8, "rebounds": 8.5, "assists": 8.6, "three_pt_pct": 0.38},
    "Shai Gilgeous-Alexander": {"position": "PG", "salary": 40_000_000, "ppg": 31.8, "rebounds": 5.2, "assists": 6.4, "three_pt_pct": 0.35},
    "Cade Cunningham":      {"position": "PG", "salary": 42_500_000, "ppg": 26.1, "rebounds": 6.4, "assists": 9.6, "three_pt_pct": 0.36},
    "Tyrese Haliburton":    {"position": "PG", "salary": 44_200_000, "ppg": 18.5, "rebounds": 3.9, "assists": 8.9, "three_pt_pct": 0.39},
    "Trae Young":           {"position": "PG", "salary": 43_000_000, "ppg": 22.4, "rebounds": 3.0, "assists": 10.8, "three_pt_pct": 0.34},
    "Damian Lillard":       {"position": "PG", "salary": 29_800_000, "ppg": 24.0, "rebounds": 4.4, "assists": 7.0, "three_pt_pct": 0.37},
    "Stephen Curry":        {"position": "PG", "salary": 59_600_000, "ppg": 24.5, "rebounds": 4.4, "assists": 6.0, "three_pt_pct": 0.41},
    "James Harden":         {"position": "PG", "salary": 36_300_000, "ppg": 21.3, "rebounds": 5.5, "assists": 8.1, "three_pt_pct": 0.35},

    # SG
    "Anthony Edwards":      {"position": "SG", "salary": 42_200_000, "ppg": 29.6, "rebounds": 5.6, "assists": 4.3, "three_pt_pct": 0.39},
    "Donovan Mitchell":     {"position": "SG", "salary": 46_400_000, "ppg": 29.0, "rebounds": 4.3, "assists": 5.7, "three_pt_pct": 0.36},
    "Devin Booker":         {"position": "SG", "salary": 53_600_000, "ppg": 25.9, "rebounds": 4.6, "assists": 6.9, "three_pt_pct": 0.35},
    "Tyrese Maxey":         {"position": "SG", "salary": 35_000_000, "ppg": 24.3, "rebounds": 3.7, "assists": 6.0, "three_pt_pct": 0.37},
    "Kon Knueppel":         {"position": "SG", "salary": 12_000_000, "ppg": 18.9, "rebounds": 4.1, "assists": 3.4, "three_pt_pct": 0.40},
    "Kyrie Irving":         {"position": "SG", "salary": 41_100_000, "ppg": 23.8, "rebounds": 4.4, "assists": 4.8, "three_pt_pct": 0.40},

    # SF
    "Jaylen Brown":         {"position": "SF", "salary": 53_100_000, "ppg": 29.4, "rebounds": 5.8, "assists": 3.9, "three_pt_pct": 0.34},
    "Jalen Johnson":        {"position": "SF", "salary": 27_500_000, "ppg": 20.1, "rebounds": 8.9, "assists": 8.2, "three_pt_pct": 0.33},
    "LeBron James":         {"position": "SF", "salary": 52_600_000, "ppg": 24.2, "rebounds": 7.5, "assists": 8.0, "three_pt_pct": 0.37},
    "Kevin Durant":         {"position": "SF", "salary": 54_700_000, "ppg": 26.6, "rebounds": 6.1, "assists": 4.3, "three_pt_pct": 0.42},
    "Jayson Tatum":         {"position": "SF", "salary": 54_100_000, "ppg": 27.8, "rebounds": 8.4, "assists": 4.6, "three_pt_pct": 0.38},
    "Paul George":          {"position": "SF", "salary": 49_200_000, "ppg": 19.5, "rebounds": 5.5, "assists": 3.5, "three_pt_pct": 0.36},
    "Michael Porter Jr.":   {"position": "SF", "salary": 31_600_000, "ppg": 20.2, "rebounds": 6.5, "assists": 2.1, "three_pt_pct": 0.40},

    # PF
    "Giannis Antetokounmpo":{"position": "PF", "salary": 55_600_000, "ppg": 30.1, "rebounds": 11.5, "assists": 6.3, "three_pt_pct": 0.28},
    "Kawhi Leonard":        {"position": "PF", "salary": 50_200_000, "ppg": 23.7, "rebounds": 6.3, "assists": 3.7, "three_pt_pct": 0.41},
    "Franz Wagner":         {"position": "PF", "salary": 28_000_000, "ppg": 24.0, "rebounds": 5.4, "assists": 4.6, "three_pt_pct": 0.34},
    "Pascal Siakam":        {"position": "PF", "salary": 46_300_000, "ppg": 21.5, "rebounds": 7.0, "assists": 3.5, "three_pt_pct": 0.35},
    "Julius Randle":        {"position": "PF", "salary": 30_900_000, "ppg": 20.4, "rebounds": 7.5, "assists": 4.9, "three_pt_pct": 0.33},
    "Zion Williamson":      {"position": "PF", "salary": 36_800_000, "ppg": 22.9, "rebounds": 6.5, "assists": 5.0, "three_pt_pct": 0.30},
    "Evan Mobley":          {"position": "PF", "salary": 38_500_000, "ppg": 18.5, "rebounds": 9.4, "assists": 3.2, "three_pt_pct": 0.34},

    # C
    "Nikola Jokic":         {"position": "C", "salary": 55_200_000, "ppg": 27.5, "rebounds": 12.9, "assists": 10.7, "three_pt_pct": 0.42},
    "Victor Wembanyama":    {"position": "C", "salary": 15_800_000, "ppg": 25.0, "rebounds": 11.1, "assists": 3.9, "three_pt_pct": 0.34},
    "Karl-Anthony Towns":   {"position": "C", "salary": 49_400_000, "ppg": 21.0, "rebounds": 11.9, "assists": 3.2, "three_pt_pct": 0.41},
    "Rudy Gobert":          {"position": "C", "salary": 43_800_000, "ppg": 12.5, "rebounds": 11.2, "assists": 1.5, "three_pt_pct": 0.0},
    "Joel Embiid":          {"position": "C", "salary": 55_200_000, "ppg": 26.0, "rebounds": 9.5, "assists": 4.2, "three_pt_pct": 0.36},
    "Domantas Sabonis":     {"position": "C", "salary": 42_000_000, "ppg": 19.5, "rebounds": 12.5, "assists": 6.0, "three_pt_pct": 0.30},
    "Anthony Davis":        {"position": "C", "salary": 54_100_000, "ppg": 24.0, "rebounds": 10.5, "assists": 3.5, "three_pt_pct": 0.28},
}

def display_franchises():
    print("\n",franchises)

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
    play = input("Would you like to play?\nyes or no\n")
    
    if play == "yes":
        display_franchises()
        team = input("\nPlease select your franchise.\n")
        franchise = team_input(team)

        while franchise is None:
            print("Franchise not found. Please try again.")
            team = input("Please select your franchise.\n")
            franchise = team_input(team)

        remaining_salary = salary_cap

        print (f"\nYour salary cap is ${salary_cap:,}.")
        print("\nBuild your 5-man roster!")
        print("Your constraint is:" , constraints[0])

        for i in range(1, 6):
            p = input(f"\nPlayer {i}. ")
            player = player_input(p)

            while player is None:
                print("Player not found. Please try again.")
                p = input(f"Player {i}. ")
                player = player_input(p)
                
            temp_salary = remaining_salary - players[player]['salary']

            while temp_salary < 0:
                print(f"You do not have enough money to draft this player! This player costs ${players[player]["salary"]:,}, please try again.\n")
                p = input(f"Player {i}. ")
                player = player_input(p)
                while player is None:
                    print("Player not found. Please try again.")
                    p = input(f"Player {i}. ")
                    player = player_input(p)
            
                temp_salary = remaining_salary - players[player]["salary"]

            remaining_salary = temp_salary
            print(f"\nYour remaining salary is ${remaining_salary:,}.\n")
            
    
    else:
        print("Thanks for checking out the game. Maybe next time!")


def main():
    print(banner)
    play_game()

main()