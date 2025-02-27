from Card import Card
import random

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit, f"{rank}_of_{suit}.png") for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.__init__()
        return self.cards.pop()