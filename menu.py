import os
#import player

exit_block = """---
0. Exit

Your choice: """

main = """=== Main ===
1. Tournament
2. Players
---
0. Exit

Your choice: """ 

goback_block = """---
0. Go back

Your choice: """

tour_menu = """=== Torunament ===
1. Print wall

9. Settings
""" + goback_block

def tournament(tour):
    while True:
        os.system('clear')
        action = input(tour_menu)
        
        if action == '0':
            break


players_menu = """=== Players ===
1. Add a new player
""" + goback_block

def players(tour):
    while True:
        os.system('clear')
        action = input(players_menu)

        if action == '0':
            break
        elif action == '1':
            add_player(tour)

def add_player(tour):
    while True:
        os.system('clear')
        print("=== Add new player ===\n")
        first_name = input("  First name: ")
        second_name = input("  Second name: ")
        country = input("  Country: ")
        level = input("  Level (15..1 kyu, 1..6 dan): ")

        try:
            tour.add_player(first_name, second_name, country, level)
            break
        except ValueError as e:
            print('', e)
            input("\nClick Enter to continue...")
        except AttributeError as e:
            print('', e)
            input("\nClick Enter to continue...")
            break


