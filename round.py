from tournament import Tournament
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
    def __init__(self, tour: Tournament) -> None:
        self.players_list = tour.active_players.copy()
        self.win_groups = tour.players_win_groups.copy()

        self.assigned_players = set()
        self.pairs = []

    @property
    def available_players(self) -> list[Player]:
        return list_cleanup(self.players_list, list(self.assigned_players))

    def suggest_pairing(self, players_list=()) -> list[tuple[Player, Player]] | None:
        # This is a recursive function
        defined_pairs = []
        assigned_players = []
        if not players_list:
            players_list = self.available_players

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
                    pairs = self.suggest_pairing(list_cleanup(players_list, [player, opponent]))
                    if pairs:
                        for pair in pairs:
                            defined_pairs.append(pair)
                        defined_pairs.append((player, opponent))
                        return defined_pairs

        return defined_pairs

    def add_pair(self, player1: Player, player2: Player) -> None:
        self.pairs.append((player1, player2))
        self.assigned_players.add(player1)
        self.assigned_players.add(player2)

    def add_suggested_pairs(self) -> None:
        for (player1, player2) in reversed(self.suggest_pairing()):
            self.add_pair(player1, player2)

    def remove_pair(self, pair_num: int) -> None:
        player1, player2 = self.pairs[pair_num]
        self.pairs.pop(pair_num)
        self.assigned_players.remove(player1)
        self.assigned_players.remove(player2)

    def clear_pairs(self) -> None:
        self.pairs.clear()
        self.assigned_players.clear()
