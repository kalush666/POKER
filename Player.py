class Player:
    def __init__(self, name, initial_balance=1000):
        self.name = name
        self.cards = []
        self.tokens = initial_balance
        self.session_start_balance = initial_balance
        self.stats = {
            "hands_played": 0,
            "hands_won": 0,
            "hands_lost": 0,
            "money_won": 0,
            "money_lost": 0,
            "biggest_win": 0,
            "biggest_loss": 0
        }

    def add_card(self, card):
        self.cards.append(card)

    def new_hand(self):
        self.cards = []
        self.stats["hands_played"] += 1

    def win_pot(self, amount):
        self.tokens += amount
        self.stats["hands_won"] += 1
        self.stats["money_won"] += amount
        if amount > self.stats["biggest_win"]:
            self.stats["biggest_win"] = amount

    def place_bet(self, amount):
        if amount > self.tokens:
            amount = self.tokens  # All-in
        self.tokens -= amount
        self.stats["money_lost"] += amount
        if amount > self.stats["biggest_loss"]:
            self.stats["biggest_loss"] = amount
        return amount

    def session_profit_loss(self):
        return self.tokens - self.session_start_balance

    def evaluate_hand(self, community_cards=None):
        """Evaluate the poker hand ranking of the player."""
        all_cards = self.cards.copy()
        if community_cards:
            all_cards.extend(community_cards)

        def get_rank_value(rank):
            rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                          '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
            return rank_order[rank]

        # Get counts of each rank and suit
        rank_counts = {}
        suits = {}
        for card in all_cards:
            if card.rank not in rank_counts:
                rank_counts[card.rank] = 0
            rank_counts[card.rank] += 1

            if card.suit not in suits:
                suits[card.suit] = 0
            suits[card.suit] += 1

        # Sort cards by rank for evaluating straights
        sorted_cards = sorted(all_cards, key=lambda card: get_rank_value(card.rank))
        sorted_ranks = [get_rank_value(card.rank) for card in sorted_cards]

        # Check for flush
        flush = any(count >= 5 for count in suits.values())

        # Check for straight
        straight = False
        for i in range(len(sorted_ranks) - 4):
            if len(set(sorted_ranks[i:i + 5])) == 5 and sorted_ranks[i + 4] - sorted_ranks[i] == 4:
                straight = True
                break

        # Special case for A-5 straight
        if not straight and 14 in sorted_ranks:  # Ace present
            ace_low = sorted_ranks.copy()
            ace_low = [1 if r == 14 else r for r in ace_low]  # Convert Ace to low
            ace_low.sort()
            for i in range(len(ace_low) - 4):
                if len(set(ace_low[i:i + 5])) == 5 and ace_low[i + 4] - ace_low[i] == 4:
                    straight = True
                    break

        # Check for straight flush
        straight_flush = straight and flush

        # Count pairs, three of a kind, etc.
        pairs = sum(1 for count in rank_counts.values() if count == 2)
        three_of_a_kind = any(count == 3 for count in rank_counts.values())
        four_of_a_kind = any(count == 4 for count in rank_counts.values())

        # Full house check
        full_house = three_of_a_kind and pairs > 0

        # Return hand ranking
        if straight_flush:
            return 8  # Straight Flush
        if four_of_a_kind:
            return 7  # Four of a Kind
        if full_house:
            return 6  # Full House
        if flush:
            return 5  # Flush
        if straight:
            return 4  # Straight
        if three_of_a_kind:
            return 3  # Three of a Kind
        if pairs >= 2:
            return 2  # Two Pair
        if pairs == 1:
            return 1  # One Pair
        return 0  # High Card
