import game, players

def list_cleanup(original, subtract):
    return [i for i in original if i not in subtract]

def players_sorted_by_scores(players):
    return sorted(players, key = lambda player: player.scores(), reverse=True)

def player_opponents_list(player, score_groups):
    # get the whole players sorted group
    players_in_group = players_sorted_by_scores([p for p in score_groups[player.wins] if p.active])
    
    # get different info about the group
    players_in_group_number = len(players_in_group)
    mediana = players_in_group_number // 2 + players_in_group_number % 2
    player_index = players_in_group.index(player)

    # for player from the second half reduce the mediana
    if player_index >= mediana:
        players_in_group_number -= player_index
        mediana = players_in_group_number // 2 + players_in_group_number % 2

    # get the second half of list below the player
    # and the rest of the list in the reversed order
    opponent_list = players_in_group[player_index + mediana:] + \
                    players_in_group[player_index + mediana - 1::-1]
    # remove alredy played opponent and the player itself from the list
    opponent_list = [op for op in opponent_list
        if op.id != player.id and op.id not in player.opponents_list()]
        
    # Add users from other groups as well going down
    for group in range(player.wins - 1, min(score_groups) - 1, -1):
        opponent_list += players_sorted_by_scores([p for p in score_groups[group]
            if p.id not in player.opponents_list() and p.active])

    return opponent_list


class Tournament:
    def __init__(self):
        self.name = ''
        self.timer = ''
        self.date = ''

        self.players_dict = {}
        game.Game.players_dict = self.players_dict

        self.players_by_scores = []
        self.players_win_groups = {}
        
        self.no_player = players.NoPlayer()
        self.players_dict[self.no_player.id] = self.no_player

        self.rounds = []

    def add_player(self, first_name, last_name, country, rating):
        new_player = players.Player(first_name, last_name, country, rating)

        if new_player.id in self.players_dict:
            raise AttributeError(f"The player is already added: '{new_player}'")
        else:
            self.players_dict[new_player.id] = new_player
        
        self.calculate_scores()

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
            players_list = self.active_players()

        for player in players_list:
            if player in assigned_players or not player.active:
                continue

            # pick up the full list of available opponents,
            player_opponents = player_opponents_list(player, self.players_win_groups)
            # leave only available for the current itteration
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
    
    @property
    def active_players(self):
        return [p for p in self.players_by_scores if p.active]

    def players_list_normalizing(self):
        if len(self.active_players()) % 2:
            if self.no_player.active:
                self.no_player.active = False
            else:
                self.no_player.active = True

    def activate_player(self, player_id):
        self.players_dict[player_id].active = True
        self.players_list_normalizing()

    def disactivate_player(self, player_id):
        self.players_dict[player_id].active = False
        self.players_list_normalizing()

    @property
    def wall(self):
        def position(player):
            if player == self.no_player:
                return 0
            else:
                players = [p for p in self.players_by_scores if p != self.no_player]
                return players.index(player) + 1

        wall = []
        for player in self.players_by_scores:
            if player == self.no_player:
                continue

            line = []
            line.append(str(position(player)))
            line.append(player.full_name)
            line.append(players.rating_list[player.rating])

            games = []
            for round in self.rounds:
                player_found = False

                for game in round:
                    if player.id not in (game.player1, game.player2):
                        continue
                    else:
                        player_found = True

                    if player.id == game.player1:
                        opponent = self.players_dict[game.player2]
                    else:
                        opponent = self.players_dict[game.player1]

                    if player.id == game.winner:
                        result = '+'
                    else:
                        result = '-'

                    games.append(position(opponent) + result)

                if not player_found:
                    games.append('--')

            line.append(games)
            line.append(str(player.wins))
            line.append(str(player.sos))
            line.append(str(player.sodos))

            wall.append(line)

        return wall

