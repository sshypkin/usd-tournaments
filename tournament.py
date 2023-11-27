import game, players

def list_cleanup(original, subtract):
    return [i for i in original if i not in subtract]

def players_sorted_by_scores(players):
    return sorted(players, key = lambda player: player.scores(), reverse=True)

def player_opponents_list(player, score_groups):
    # pick up a list of available opponents within the same win group
    opponents_in_group = players_sorted_by_scores([p for p in score_groups[player.wins]
        if p.id != player.id and p.id not in player.opponents_list()])

    opponents_in_group_number = len(opponents_in_group)
    if opponents_in_group_number > 1:
        # divide the list by half and reorder it
        opponent_list = opponents_in_group[opponents_in_group_number // 2:] + \
                        opponents_in_group[opponents_in_group_number // 2-1::-1]
    elif opponents_in_group_number:
        opponent_list = opponents_in_group
    else:
        opponent_list = []

    # Add users from other groups as well going down
    for group in range(player.wins - 1, min(score_groups) - 1, -1):
        opponent_list += players_sorted_by_scores([p for p in score_groups[group]
            if p.id not in player.opponents_list()])

    return opponent_list


class Tournament:
    def __init__(self, name):
        self.name = name
        self.players_dict = {}
        game.Game.players_dict = self.players_dict
        self.players_by_scores = []
        self.players_win_groups = {}
        self.rounds = []

    def add_player(self, first_name, last_name, country, rating):
        new_player = players.Player(first_name, last_name, country, rating)
        self.players_dict[new_player.id] = new_player

    def calculate_scores(self):
        self.players_win_groups = {}
        for player in self.players_dict.values():
            player.calculate_scores()

            if player.wins not in self.players_win_groups:
                self.players_win_groups[player.wins] = []

            self.players_win_groups[player.wins].append(player)

        self.players_by_scores = players_sorted_by_scores(self.players_dict.values())

    def suggest_paring(self, players_list = []):
        # This is a recursuve function
        defined_pairs = []
        assigned_players = []
        if not players_list:
            players_list = self.players_by_scores

        for player in players_list:
            if player in assigned_players:
                continue

            # pick up the full list of available opponents
            player_opponents = player_opponents_list(player, self.players_win_groups)
            # and leave only available for the current itteration
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
                    pairs = self.suggest_paring(list_cleanup(players_list, (player, opponent)))
                    if pairs:
                        for pair in pairs:
                            defined_pairs.append(pair)
                        defined_pairs.append((player, opponent))
                        return defined_pairs

        return defined_pairs

    def add_round(self, suggested_pairs):
        games = []
        for player1, player2 in suggested_pairs:
            games.append(game.Game(player1.id, player2.id))

        self.rounds.append(games)






