class Game:
    players_dict = {}

    def __init__(self, player1_id, player2_id):
        if player1_id not in self.players_dict.keys() and player2_id not in self.players_dict.keys():
            raise ValueError(f"Players '{player1_id}' or '{player2_id}' are not in the players list: ",
                             self.players_dict.keys())

        self.id = f"{player1_id}:{player2_id}"
        self.player1 = player1_id
        self.player2 = player2_id

        self.players_dict[player1_id].games.append(self)
        self.players_dict[player2_id].games.append(self)
        
        if player1_id == 'free':
            self.set_winner(player2_id)
        elif player2_id == 'free':
            self.set_winner(player1_id)
        else:
            self.winner = None

    def set_winner(self, player_id):
        if player_id not in (self.player1, self.player2):
            raise ValueError(f"Player '{player_id}' is not assigned to that game ('{self.player1}', '{self.player2}')")
        
        self.winner = player_id
        self.players_dict[player_id].calculate_wins()

    def __str__(self):
        return f"{self.player1} vs {self.player2}, {self.winner} wins."
