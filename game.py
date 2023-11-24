class Game:
    player_dict = {}

    def __init__(self, player1, player2):
        if player1 in self.player_dict.keys() and player2 in self.player_dict.keys():
            self.player1 = player1
            self.player2 = player2
            self.id = f"{player1}:{player2}"
            self.winner = None

            self.player_dict[player1].games.append(self)
            self.player_dict[player2].games.append(self)

        else:
            raise ValueError(f"Players '{player1}' or '{player2}' are not in the players list: ", self.player_dict.keys())

    def set_winner(self, player_id):
        if player_id in (self.player1, self.player2):
            self.winner = player_id
            self.player_dict[player_id].calculate_wins()
        else:
            raise ValueError(f"Player '{player}' is not assigned to that game ('{self.player1}', '{self.player2}')")

    def __str__(self):
        return f"{self.player1} vs {self.player2}, {self.winner} wins."
