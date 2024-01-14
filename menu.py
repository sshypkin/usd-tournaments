import string

from tournament import Tournament
from round import Round
from players import Player, NoPlayer
import os


def wait_to_continue():
    input("\nClick Enter to continue...")


exit_block = """---
0. Exit

Your choice: """

main = """=== Main ===
1. Tournament
2. Players
3. Rounds
---
0. Exit

Your choice: """

tournament_menu = """=== Tournament ===
1. Print wall
2. Print result for FESA

9. Settings
""" + exit_block


def tournament(tour):
    while True:
        os.system('clear')
        action = input(tournament_menu)

        if action == '0':
            break
        elif action == '1':
            print_wall(tour)
        elif action == '2':
            print_fesa(tour)
        elif action == '9':
            tournament_settings(tour)


def print_wall(tour: Tournament):
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
        (w_num, w_pid, w_rank, w_rounds, w_points, w_sos, w_sodos) = line
        player_full_name = tour.players_dict[w_pid].full_name

        if len(w_num) > num_len:
            num_len = len(w_num)
        if len(player_full_name) > name_len:
            name_len = len(player_full_name)
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
    round_numbers_line = ''
    if rounds_num:
        round_line = '-' * result_len + ' '
        rounds_line = round_line * rounds_num
        rounds_line = rounds_line[:-1]

        for i in range(1, rounds_num + 1):
            round_numbers_line += str(i).center(result_len) + ' '
        round_numbers_line = round_numbers_line[:-1]
    else:
        rounds_line = ''

    print(tour.date)
    print(tour.name)
    print("Time control:", tour.timer)

    print('-' * num_len, '-' * name_len, '-' * rank_len, rounds_line,
          '-' * points_len, '-' * sos_len, '-' * sodos_len)
    print(num.rjust(num_len), name.ljust(name_len), rank.rjust(rank_len), round_numbers_line,
          points.rjust(points_len), sos.rjust(sos_len), sodos.rjust(sodos_len))
    print('-' * num_len, '-' * name_len, '-' * rank_len, rounds_line,
          '-' * points_len, '-' * sos_len, '-' * sodos_len)

    for line in wall:
        (w_num, w_pid, w_rank, w_rounds, w_points, w_sos, w_sodos) = line
        player_full_name = tour.players_dict[w_pid].full_name

        rounds = ''
        for current_round in w_rounds:
            rounds += str(current_round).rjust(result_len) + ' '
        rounds = rounds[:-1]

        print(w_num.rjust(num_len), player_full_name.ljust(name_len), w_rank.rjust(rank_len),
              rounds.rjust(len(rounds_line)),
              w_points.rjust(points_len), w_sos.rjust(sos_len), w_sodos.rjust(sodos_len))

    wait_to_continue()


def print_fesa(tour: Tournament):
    os.system('clear')
    wall = tour.wall

    print(tour.date)
    print(tour.name)
    print("Time control:", tour.timer)

    rounds_line = ''
    for i in range(1, len(tour.rounds) + 1):
        rounds_line += str(i) + ' '
    rounds_line = rounds_line[:-1]
    print('Nr Name Nat', rounds_line, 'Pts')

    for line in wall:
        (w_num, w_pid, w_rank, w_rounds, w_points, w_sos, w_sodos) = line

        rounds_line = ''
        for current_round in w_rounds:
            if current_round == '0+':
                current_round = 'free'
            elif current_round == '--':
                current_round = '-'
            rounds_line += current_round + ' '
        rounds_line = rounds_line[:-1]

        print(f"{w_num} [{tour.players_dict[w_pid].second_name}] [{tour.players_dict[w_pid].first_name}] "
              f"{tour.players_dict[w_pid].country} [{rounds_line}] {w_points}")

    wait_to_continue()


def tournament_settings(tour):
    print("=== Tournament settings ===\n")
    tour.name = input("  Tournament name: ")
    tour.timer = input("  Round time: ")
    tour.date = input("  Date(s): ")


players_menu = """=== Players ===
1. Add a new player
""" + exit_block


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


rounds_menu = """=== Rounds ===
1. Show rounds
2. Add a new round
3. Edit round
""" + exit_block


def rounds(tour: Tournament) -> None:
    while True:
        os.system('clear')
        action = input(rounds_menu)

        if action == '0':
            break
        elif action == '1':
            show_rounds(tour)
        elif action == '2':
            new_round(tour)
        elif action == '3':
            edit_round(tour)


def show_rounds(tour: Tournament) -> None:
    if tour.rounds_tmp:
        os.system('clear')
        round_num = 1

        for round_item in tour.rounds_tmp:
            print(f"Round {round_num}")
            print("\tSuggested pairing")
            print("\t" + "-" * 10)
            for player1, player2 in round_item.suggested_pairing:
                print(f"\t{player1.full_name} vs {player2.full_name}")
            round_num += 1

        wait_to_continue()

    else:
        while True:
            os.system('clear')
            print("No rounds found.")
            answer = input("Would you like to add one? (y/n) ")
            if answer == 'y':
                new_round(tour)
                break
            elif answer == 'n':
                break


def new_round(tour: Tournament):
    os.system('clear')
    current_round = Round(tour)
    tour.rounds_tmp.append(current_round)

    print("New round successfully added.")
    wait_to_continue()


edit_round_menu = string.Template("""=== Edit round $number ===
1. Edit pairs 
""" + exit_block)


def edit_round(tour: Tournament) -> None:
    rounds_num = len(tour.rounds_tmp)
    if not rounds_num:
        print("No rounds to edit. Please create a new one first.")
        return

    # Pick up a round
    rounds_list = list(range(1, rounds_num + 1))
    rounds_list = ', '.join(str(i) for i in rounds_list)
    current_round = None
    while True:
        os.system('clear')
        print("Available rounds:", rounds_list)
        round_num = input("\nChoose a round: ")
        if not round_num.isnumeric():
            continue
        round_num = int(round_num)

        if 1 <= round_num <= rounds_num:
            current_round = tour.rounds_tmp[round_num - 1]
            break

    # Edit round
    while True:
        os.system('clear')
        action = input(edit_round_menu.substitute(number=round_num))
        if action == '0':
            break
        elif action == '1':
            edit_pairs(current_round)


edit_pairs_menu = """
Choose an action:
---
1. View suggested pairing
2. Use suggested pairing
3. View current pairs
4. Add a pair
5. Remove a pair
6. Remove all pairs 
""" + exit_block


def print_round_players(current_round: Round, list_type: str) -> None:
    length = 10
    player_list = []

    if list_type == 'Available':
        player_list = current_round.available_players
    elif list_type == 'Active':
        player_list = current_round.players_list

    print(f"\n{list_type} players:")
    print('-' * length)
    for n, player in enumerate(player_list):
        if player.full_name == 'free':
            continue
        print(f"{n + 1}. {player}, {player.wins} wins")
    print('-' * length)


def print_round_pairs(current_round: Round, pair_type: str) -> None:
    length = 10
    pairs = list()
    players_list = list()

    if pair_type == 'Suggested':
        pairs = reversed(current_round.suggest_pairing())
        players_list = current_round.available_players
    elif pair_type == 'Current':
        pairs = current_round.pairs
        players_list = current_round.players_list

    print(f"\n{pair_type} pairs:")
    print('-' * length)
    if pairs:
        for n, (player1, player2) in enumerate(pairs):
            if player2.full_name == 'free':
                print(f"pair {n + 1}: {player1} ({players_list.index(player1) + 1}) is free")
                continue
            print(f"pair {n + 1}: {player1} ({players_list.index(player1) + 1}) -> X "
                  f"<- ({players_list.index(player2) + 1}) {player2}")
    else:
        print(None)
    print('-' * length)


def edit_pairs(current_round: Round) -> None:
    while True:
        os.system('clear')
        # print_round_players(current_round, 'Active')

        action = input(edit_pairs_menu)
        if action == '0':
            break

        elif action == '1':
            # View suggested pairing
            print_round_players(current_round, 'Available')
            print_round_pairs(current_round, 'Suggested')

        elif action == '2':
            # Use suggested pairing
            current_round.add_suggested_pairs()
            print("Done")

        elif action == '3':
            # View current pairs
            print_round_players(current_round, 'Active')
            print_round_pairs(current_round, 'Current')

        elif action == '4':
            # Add a pair
            print_round_players(current_round, 'Available')
            print_round_pairs(current_round, 'Suggested')
            print()
            print("Set a pair")
            player1_pos = input("1st player's position: ")
            player2_pos = input("2nd player's position: ")
            player1 = current_round.available_players[int(player1_pos) - 1]
            player2 = current_round.available_players[int(player2_pos) - 1]
            current_round.add_pair(player1, player2)
            print("Done")

        elif action == '5':
            # Remove a pair
            print_round_pairs(current_round, 'Current')
            print()
            pair_num = input("Remove pair number: ")
            current_round.remove_pair(int(pair_num) - 1)
            print("Done")

        elif action == '6':
            # Remove all pairs
            current_round.clear_pairs()
            print("Done")

        wait_to_continue()
