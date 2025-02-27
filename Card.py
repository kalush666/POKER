class Card:
    def __init__(self, rank, suit, imgSrc):
        self.rank = rank
        self.suit = suit
        self.imgSrc = imgSrc

    def __str__(self):
        return f"{self.rank} of {self.suit}"