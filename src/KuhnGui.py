from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from Player import Player
from Game import Game
import os

class PokerTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kuhn Poker")
        self.setGeometry(100, 100, 800, 600)

        self.game = Game()
        self.game.shuffle_and_deal()

        # Set the central widget and the general layout
        self.general_layout = QVBoxLayout()
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)

        # Display for the pot size
        self.pot_label = QLabel(f"Pot Size: {self.game.pot}")
        self.general_layout.addWidget(self.pot_label)

        # Create the table widget and add it to the layout
        self.table_widget = self._create_table_widget()
        self.general_layout.addWidget(self.table_widget)

    def _create_table_widget(self):
        table_widget = QWidget()
        table_layout = QVBoxLayout()

        # Position of the top player
        self.top_player = PlayerArea(self, self.game, player=self.game.players[1])
        table_layout.addWidget(self.top_player)

        # Add the bottom player (user) area to the layout
        self.bottom_player = PlayerArea(self, self.game, player=self.game.players[0])
        table_layout.addWidget(self.bottom_player)

        table_widget.setLayout(table_layout)
        return table_widget
    
class PlayerArea(QWidget):
    def __init__(self, tablegui, game: Game, player: Player):
        super().__init__()
        self.player = player
        self.game = game
        self.tablegui = tablegui

        self.layout = QHBoxLayout() if player.name == "Human" else QVBoxLayout()

        self.card_images = {
            'J': QPixmap(os.path.join('./Images', 'jack.png')),
            'Q': QPixmap(os.path.join('./Images', 'queen.png')),
            'K': QPixmap(os.path.join('./Images', 'king.png')),
            'Hidden': QPixmap(os.path.join('./Images', 'bot.png'))
        }

        self.card_label = QLabel()
        
        if self.player.name == 'Bot':
            self.card_label.setPixmap(self.card_images['Hidden'])
        else:
            self.card_label.setPixmap(self.card_images[self.player.hand])


        self.chips_label = QLabel(f'Chips: {player.chip_count}')
        self.layout.addWidget(self.card_label)
        self.layout.addWidget(self.chips_label)

        if self.player.name == 'Human':    
            self.check_fold_button = QPushButton('Check/Fold')
            self.bet_call_button = QPushButton('Bet/Call')
            self.layout.addWidget(self.check_fold_button)
            self.layout.addWidget(self.bet_call_button)
            self.check_fold_button.clicked.connect(self.check_fold)
            self.bet_call_button.clicked.connect(self.bet_call)

        self.setLayout(self.layout) 

    def check_fold(self):
        if self.game.betting_history:
            self.game.player_fold()
        else:
            self.game.player_check()
        self.update_game_state()

    def bet_call(self):
        if self.game.betting_history:
            self.game.player_call(1)
        else:
            self.game.player_bet(1)
        self.update_game_state()

    def update_game_state(self):
        self.tablegui.pot_label.setText(f'Pot Size: {self.game.pot}')
        self.tablegui.bottom_player.card_label.setPixmap(self.card_images[self.player.hand])
        self.tablegui.top_player.chips_label.setText(f'Chips: {self.tablegui.top_player.player.chip_count}')
        self.tablegui.bottom_player.chips_label.setText(f'Chips: {self.tablegui.bottom_player.player.chip_count}')



if __name__ == '__main__':
    app = QApplication([])
    poker_table = PokerTable()
    poker_table.show()
    app.exec_()