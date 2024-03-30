from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class PokerTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kuhn Poker")
        self.setGeometry(100, 100, 800, 600)

        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Create the table widget and add it to the layout
        self.tableWidget = self._createTableWidget()
        self.generalLayout.addWidget(self.tableWidget)

    def _createTableWidget(self):
        table_widget = QWidget()
        table_layout = QVBoxLayout()

        # Position of the top player
        self.topPlayer = PlayerArea(position='top')
        table_layout.addWidget(self.topPlayer)

        # Add the bottom player (user) area to the layout
        self.bottomPlayer = PlayerArea(position='bottom')
        table_layout.addWidget(self.bottomPlayer)

        table_widget.setLayout(table_layout)
        return table_widget
    
class PlayerArea(QWidget):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.layout = QHBoxLayout()

        self.cardLabel = QLabel('Card')
        self.layout.addWidget(self.cardLabel)

        self.chipsLabel = QLabel('Chips: 100')
        self.layout.addWidget(self.chipsLabel)
        
        if position == 'bottom':
            self.foldButton = QPushButton('Fold')
            self.callButton = QPushButton('Call')
            self.raiseButton = QPushButton('Raise')
            self.layout.addWidget(self.foldButton)
            self.layout.addWidget(self.callButton)
            self.layout.addWidget(self.raiseButton)

        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication([])
    poker_table = PokerTable()
    poker_table.show()
    app.exec_()