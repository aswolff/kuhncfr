class Player:
    def __init__(self, name: str, chip_count: int = 10, dealer: bool = True):
        self.name = name
        self.hand = None
        self.chip_count = chip_count
        self.has_folded = False
        self.dealer = True

    def receive_card(self, card: str) -> None:
        self.hand = card

    def bet(self, amount: int) -> None:
        self.chip_count -= amount

    def fold(self) -> bool:
        self.has_folded = True

    def call(self, amount: int) -> None:
        return self.place_bet(amount)
    
    def check(self):
        pass

    def reset_for_new_round(self) -> None:
        self.hand = None
        self.has_folded = False

    def show_hand(self) -> str:
        return self.hand
    
    def switch_dealer(self) -> None:
        self.dealer = not self.dealer
