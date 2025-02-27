import tkinter as tk
from PIL import Image, ImageTk
from Deck import Deck
from Player import Player
import os

class PokerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Game")
        self.deck = Deck()
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = 0
        self.pot = 0
        self.community_cards = []
        self.card_images = []

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Load and display the background image
        image_path = os.path.join(os.path.dirname(__file__), "table.jpg")
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)

        self.draw_hand_button = tk.Button(root, text="Draw Hand", command=self.start_game)
        self.draw_hand_button.pack()

        # Add Raise, Check, and Fold buttons
        self.raise_button = tk.Button(root, text="Raise", command=self.raise_bet)
        self.raise_button.pack(side=tk.LEFT, padx=10)

        self.check_button = tk.Button(root, text="Check", command=self.check_bet)
        self.check_button.pack(side=tk.LEFT, padx=10)

        self.fold_button = tk.Button(root, text="Fold", command=self.fold_hand)
        self.fold_button.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(root, text="Welcome to Poker Game!")
        self.status_label.pack()

    def start_game(self):
        self.deck.shuffle()
        self.community_cards = []
        for player in self.players:
            player.new_hand()
            for _ in range(2):
                player.add_card(self.deck.draw_card())
        self.display_hand()

    def display_hand(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)
        self.card_images = []

        player = self.players[self.current_player_index]
        for i, card in enumerate(player.cards):
            # Construct the correct path to the card image
            card_path = os.path.join(os.path.dirname(__file__), "cards", card.imgSrc)
            card_path = os.path.abspath(card_path)  # Convert to absolute path
            img = Image.open(card_path)
            img = img.resize((100, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.card_images.append(photo)
            self.canvas.create_image(150 * i + 50, 300, image=photo)

        self.status_label.config(text=f"{player.name}'s turn. Pot: {self.pot} tokens")

    def raise_bet(self):
        self.pot += 10
        self.next_turn()

    def check_bet(self):
        self.next_turn()

    def fold_hand(self):
        self.players.pop(self.current_player_index)
        if len(self.players) == 1:
            self.status_label.config(text=f"{self.players[0].name} wins the pot of {self.pot} tokens!")
        else:
            self.next_turn()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.display_hand()

if __name__ == "__main__":
    root = tk.Tk()
    game = PokerGame(root)
    root.mainloop()