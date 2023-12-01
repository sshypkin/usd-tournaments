rating_list = ['15 kyu', '14 kyu', '13 kyu', '12 kyu', '11 kyu', '10 kyu', '9 kyu', '8 kyu', '7 kyu', '6 kyu', '5 kyu', '4 kyu', '3 kyu', '2 kyu', '1 kyu', '1 dan', '2 dan', '3 dan', '4 dan', '5 dan', '6 dan']

class Player:
    def __init__(self, first_name, second_name, country, rating):
        if first_name:
            self.first_name = first_name
        else:
            raise ValueError(f"\nFirst name should not be empty: '{first_name}'")
        
        if second_name:
            self.second_name = second_name
        else:
            raise ValueError(f"\nSecond name should not be empty: '{second_name}'")
        
        if country:
            self.country = country
        else:
            raise ValueError(f"\nCountry should not be empty: '{country}'")

        if rating in rating_list:
            self.rating = rating_list.index(rating)
        else:
            raise ValueError(f"\nRating '{rating}' is not in the rating list:\n{rating_list}")

        self.id = f"{second_name}{first_name}{country}{self.rating}"
        self.full_name = f"{second_name} {first_name}"
        self.games = []
        self.wins = 0
        self.sos = 0
        self.sodos = 0
        self.active = True

    def scores(self):
        return (self.wins, self.sos, self.sodos, self.rating)

    def calculate_wins(self):
        self.wins = 0
        for game in self.games:
            if game.winner == self.id:
                self.wins += 1

    def calculate_scores(self):
        self.sos = 0
        self.sodos = 0

        for game in self.games:
            if game.player1 == self.id:
                opponent = game.player2
            else:
                opponent = game.player1

            self.sos += game.players_dict[opponent].wins
            if game.winner == self.id:
                self.sodos += game.players_dict[opponent].wins

    def opponents_list(self):
        opponents = []

        for game in self.games:
            if game.player1 == self.id:
                opponent = game.player2
            else:
                opponent = game.player1
            
            opponents.append(opponent)

        return opponents

    def __str__(self):
        return f"{self.full_name}, {self.country}, {rating_list[self.rating]}"


class NoPlayer(Player):
    def __init__(self):
        self.first_name = ''
        self.second_name = ''
        self.full_name = "free"
        self.country = ''
        self.id = self.full_name
        self.rating = 0
        self.games = []
        self.wins = 0
        self.sos = 0
        self.sodos = 0
        self.active = False

    def calculate_wins(self):
        pass

    def calculate_scores(self):
        pass

    def __str__(self):
        return self.full_name

