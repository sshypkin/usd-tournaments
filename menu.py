import os
#import player

def wait_to_continue():
    input("\nClick Enter to continue...")

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

tour_menu = """=== Tournament ===
1. Print wall

9. Settings
""" + goback_block

def tournament(tour):
    while True:
        os.system('clear')
        action = input(tour_menu)
        
        if action == '0':
            break
        elif action == '1':
            print_wall(tour)
        elif action == '9':
            tournament_settings(tour)

def print_wall(tour):
    os.system('clear')
    wall = tour.wall

    num = "№"
    num_len = len(num)
    name = "Name"
    name_len = len(name)
    rank = "Rank"
    rank_len = len(rank)
    points = "Points"
    points_len = len(points)
    sos = "SOS"
    sos_len = len(sos)
    sodos = "SODOS"
    sodos_len = len(sodos)

    for line in wall:
        (w_num, w_name, w_rank, w_rounds, w_points, w_sos, w_sodos) = line
        if len(w_num) > num_len:
            num_len = len(w_num)
        if len(w_name) > name_len:
            name_len = len(w_name)
        if len(w_rank) > rank_len:
            rank_len = len(w_rank)
        if len(w_points) > points_len:
            points_len = len(w_points)
        if len(w_sos) > sos_len:
            sos_len = len(w_sos)
        if len(w_sodos) > sodos_len:
            sodos_len = len(w_sodos)
    result_len = num_len + 1

    rounds_num = len(tour.rounds)
    if rounds_num:
        round_line = '-' * result_len + ' '
        rounds_line = round_line * rounds_num
        rounds_line = rounds_line[:-1]

        rounds_line_num = ''
        for r in range(1, rounds_num + 1):
            rounds_line_num = str(r).rjust(result_len) + ' '
        # rounds_line_num = rounds_line_num[:-1]

        round_numbers_line = ''
        for i in range(1, rounds_num + 1):
            round_numbers_line += str(i).center(result_len) + ' '
        round_numbers_line = round_numbers_line[:-1]
    else:
        rounds_line = ''
        # rounds_line_num = ''

    print(tour.date)
    print(tour.name)
    print("Round time:", tour.timer)

    print('-' * num_len, '-' * name_len, '-' * rank_len, rounds_line,
            '-' * points_len, '-' * sos_len, '-' * sodos_len)
    print(num.rjust(num_len), name.ljust(name_len), rank.rjust(rank_len), round_numbers_line,
            points.rjust(points_len), sos.rjust(sos_len), sodos.rjust(sodos_len))
    print('-' * num_len, '-' * name_len, '-' * rank_len, rounds_line,
                        '-' * points_len, '-' * sos_len, '-' * sodos_len)

    for line in wall:
        (w_num, w_name, w_rank, w_rounds, w_points, w_sos, w_sodos) = line

        rounds = ''
        for round in w_rounds:
            rounds += str(round).rjust(result_len) + ' '
        rounds = rounds[:-1]

        print(w_num.rjust(num_len), w_name.ljust(name_len), w_rank.rjust(rank_len), rounds.rjust(len(rounds_line)),
                w_points.rjust(points_len), w_sos.rjust(sos_len), w_sodos.rjust(sodos_len))

    wait_to_continue()


def tournament_settings(tour):
    print("=== Tournament settings ===\n")
    tour.name = input("  Tournament name: ")
    tour.timer = input("  Round time: ")
    tour.date = input("  Date(s): ")


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
            wait_to_continue()
        except AttributeError as e:
            print('', e)
            wait_to_continue()
            break


