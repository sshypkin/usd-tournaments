from typing import List, Tuple, Any

# from tournament import Tournament
from players import Player


def list_cleanup(original: list, subtract: list) -> list:
    return [i for i in original if i not in subtract]


def players_sorted_by_scores(players: list[Player]) -> list:
    return sorted(players, key=lambda player: player.scores(), reverse=True)


def get_median(length: int) -> int:
    return length // 2 + length % 2  # divide by 2 rounds up


def player_opponents_list(player: Player, score_groups: dict) -> list:
    # get the whole players sorted group
    players_in_group = players_sorted_by_scores([p for p in score_groups[player.wins] if p.active])

    # get different info about the group
    players_in_group_number = len(players_in_group)
    median = get_median(players_in_group_number)
    player_index = players_in_group.index(player)

    # for player from the second half reduce the median
    if player_index >= median:
        players_in_group_number -= player_index
        median = get_median(players_in_group_number)

    # get the second half of list below the player and the rest of the list in the reversed order
    opponent_list = players_in_group[player_index + median:] + players_in_group[player_index + median - 1::-1]
    # remove already played opponent and the player itself from the list
    opponent_list = [op for op in opponent_list
                     if op.id != player.id and op.id not in player.opponents_list()]

    # Add users from groups below as well
    for group in range(player.wins - 1, min(score_groups) - 1, -1):
        opponent_list += players_sorted_by_scores([p for p in score_groups[group]
                                                   if p.id not in player.opponents_list() and p.active])

    return opponent_list


class Round:
    def __init__(self, active_players: list[list], win_groups: dict) -> None:
        self.players_list = active_players.copy()
        self.available_players = self.players_list.copy()
        self.assigned_players = []
        self.win_groups = win_groups.copy()
        self.suggested_pairing = self.suggest_paring()
        self.pairs = []

    def suggest_paring(self, players_list=()) -> list[tuple[any, any]] | None:
        # This is a recursive function
        defined_pairs = []
        assigned_players = []
        if not players_list:
            players_list = self.players_list

        for player in players_list:
            if player in assigned_players or not player.active:
                continue

            # pick up the full list of available opponents,
            player_opponents = player_opponents_list(player, self.win_groups)
            # leave only available for the current iteration
            player_opponents = [op for op in player_opponents if op in players_list]

            opponents_number = len(player_opponents)
            if not opponents_number:
                return None

            elif opponents_number == 1:
                defined_pairs.append((player, player_opponents[0]))
                assigned_players.append(player)
                assigned_players.append(player_opponents[0])

            else:
                for opponent in player_opponents:
                    pairs = self.suggest_paring(list_cleanup(players_list, [player, opponent]))
                    if pairs:
                        for pair in pairs:
                            defined_pairs.append(pair)
                        defined_pairs.append((player, opponent))
                        return defined_pairs

        return defined_pairs
