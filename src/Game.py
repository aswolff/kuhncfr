import random
from Player import Player


class Game:
    def __init__(self):
        self.deck = ['J', 'Q', 'K']
        self.players = [Player("Human", 10, True), Player("Bot", 10, False)]
        self.current_player = 0  # 0 for Human, 1 for Bot
        self.pot = 0
        self.betting_history = []

    def shuffle_and_deal(self):
        random.shuffle(self.deck)
        for player in self.players:
            player.receive_card(self.deck.pop())
            player.chip_count -= 1
            self.pot += 1
        self.current_player = 1 if self.players[0].dealer else 0

    def switch_turn(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def player_bet(self, amount):
        player = self.players[self.current_player]
        player.bet(amount)
        self.pot += amount
        self.betting_history.append((self.current_player, 'bet', amount))
        self.switch_turn()

    def player_call(self, amount):
        player = self.players[self.current_player]
        player.call(amount)
        self.pot += amount
        self.betting_history.append((self.current_player, 'call', amount))
        self.payout()

    def player_check(self):
        player = self.players[self.current_player]
        player.check()
        self.betting_history.append((self.current_player, 'check'))
        if not player:
            self.switch_turn()
        else:
            self.determine_winner()

    def player_fold(self):
        player = self.players[self.current_player]
        player.fold()
        self.betting_history.append((self.current_player, 'fold'))
        self.payout()

    def determine_winner(self):
        if self.players[0].has_folded:
            return 1
        elif self.players[1].has_folded:
            return 0
        player_0_card_rank = 'JQK'.index(self.players[0].show_hand())
        player_1_card_rank = 'JQK'.index(self.players[1].show_hand())

        if player_0_card_rank > player_1_card_rank:
            return 0  # Player 0 wins
        else:
            return 1  # Player 1 wins

    def payout(self):
        winner_index = self.determine_winner()
        winner = self.players[winner_index]
        # Add the pot to the winner's chip count
        winner.chip_count += self.pot
        print(f"{winner.name} wins the pot of size {self.pot}")
        # Reset pot and player bet amounts for the next round
        self.pot = 0
        self.deck = ['J', 'Q', 'K']
        for player in self.players:
            player.switch_dealer()
            player.reset_for_new_round()