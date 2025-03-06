# In PokerGame.py (modifications)
# Add to imports
from network import PokerClient

# Modify the PokerGame class
class PokerGame:
    def __init__(self, root, user_data=None):
        # ... existing init code ...
        self.network = PokerClient(self)  # Add this line
        # Remove AI players and local game setup
        self.players = [Player("You", initial_balance)]  # Only human player

    # Replace game actions with network commands
    def raise_bet(self):
        amount = self.bet_amount.get()
        self.network.send_action(f"raise {amount}")

    def call_bet(self):
        self.network.send_action("call")

    def fold_hand(self):
        self.network.send_action("fold")

    def handle_server_message(self, message):
        # Process server messages and update GUI
        if "community_cards" in message:
            self.update_community_cards(message)
        elif "your_cards" in message:
            self.update_player_cards(message)
        # Add more message handling as needed
        self.root.after(0, self.update_gui)

    def update_gui(self):
        # Update cards, pot, balances based on game state
        self.display_game_state()
        self.update_stats_display()