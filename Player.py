# Player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.tokens = 0

    def add_card(self, card):
        self.cards.append(card)

    def new_hand(self):
        self.cards = []

    def evaluate_hand(self):
        def is_straight_flush(cards):
            if len(cards) < 5:
                return False
            rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
            cards = sorted(cards, key=lambda card: rank_order[card.rank])
            suits = [card.suit for card in cards]
            if len(set(suits)) != 1:
                return False
            for i in range(len(ranks) - 4):
                if ranks[i:i+5] == list(range(ranks[i], ranks[i] + 5)):
                    return True
            return False

        def is_four_of_a_kind(cards):
            rank_counts = {card.rank: 0 for card in cards}
            for card in cards:
                rank_counts[card.rank] += 1
            return 4 in rank_counts.values()

        def is_full_house(cards):
            rank_counts = {card.rank: 0 for card in cards}
            for card in cards:
                rank_counts[card.rank] += 1
            return 3 in rank_counts.values() and 2 in rank_counts.values()

        def is_flush(cards):
            suits = [card.suit for card in cards]
            return len(set(suits)) == 1

        def is_straight(cards):
            rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
            ranks = [rank_order[card.rank] for card in cards]
            for i in range(len(ranks) - 4):
                if ranks[i:i+5] == list(range(ranks[i], ranks[i] + 5)):
                    return True
            return False

        def is_three_of_a_kind(cards):
            rank_counts = {card.rank: 0 for card in cards}
            for card in cards:
                rank_counts[card.rank] += 1
            return 3 in rank_counts.values()

        def is_two_pair(cards):
            rank_counts = {card.rank: 0 for card in cards}
            for card in cards:
                rank_counts[card.rank] += 1
            return list(rank_counts.values()).count(2) == 2

        def is_one_pair(cards):
            rank_counts = {card.rank: 0 for card in cards}
            for card in cards:
                rank_counts[card.rank] += 1
            return 2 in rank_counts.values()

        if is_straight_flush(self.cards):
            return 8
        if is_four_of_a_kind(self.cards):
            return 7
        if is_full_house(self.cards):
            return 6
        if is_flush(self.cards):
            return 5
        if is_straight(self.cards):
            return 4
        if is_three_of_a_kind(self.cards):
            return 3
        if is_two_pair(self.cards):
            return 2
        if is_one_pair(self.cards):
            return 1
        return 0