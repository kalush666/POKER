import tkinter as tk
from tkinter import ttk, messagebox
from Deck import Deck
from Player import Player
from network import PokerClient
from Card import Card
from FinancialTips import FinancialTips
import random


class PokerGame:
    def __init__(self, root, user_data=None):
        self.root = root
        self.root.title("Poker Game")
        self.root.geometry("800x600")

        # Initialize game variables
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.player_turn = 0
        self.round = 0  # 0: pre-flop, 1: flop, 2: turn, 3: river

        # Initialize players (default to local game if no network)
        initial_balance = 1000
        self.players = [Player("You", initial_balance)]

        # Add AI players for local game
        self.ai_players = []
        if not user_data:  # Local game
            self.ai_players = [
                Player("AI Player 1", initial_balance),
                Player("AI Player 2", initial_balance),
                Player("AI Player 3", initial_balance)
            ]
            self.players.extend(self.ai_players)

        # Try to connect to network game
        try:
            self.network = PokerClient(self)
            self.networked_game = True
        except Exception as e:
            print(f"Running in local mode: {e}")
            self.networked_game = False

        # Create GUI elements
        self.create_gui()

        # Start a new game
        self.start_new_hand()

        # Display a financial tip
        self.display_financial_tip()

    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Community cards frame
        self.community_frame = ttk.LabelFrame(main_frame, text="Community Cards")
        self.community_frame.pack(fill=tk.X, pady=10)

        self.community_labels = []
        for i in range(5):
            label = ttk.Label(self.community_frame, text="", width=10, borderwidth=1, relief="solid")
            label.grid(row=0, column=i, padx=5, pady=5)
            self.community_labels.append(label)

        # Player cards frame
        self.player_frame = ttk.LabelFrame(main_frame, text="Your Cards")
        self.player_frame.pack(fill=tk.X, pady=10)

        self.player_labels = []
        for i in range(2):
            label = ttk.Label(self.player_frame, text="", width=10, borderwidth=1, relief="solid")
            label.grid(row=0, column=i, padx=5, pady=5)
            self.player_labels.append(label)

        # Game info frame
        info_frame = ttk.LabelFrame(main_frame, text="Game Info")
        info_frame.pack(fill=tk.X, pady=10)

        ttk.Label(info_frame, text="Pot:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.pot_label = ttk.Label(info_frame, text="$0")
        self.pot_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(info_frame, text="Current Bet:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.current_bet_label = ttk.Label(info_frame, text="$0")
        self.current_bet_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(info_frame, text="Your Balance:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.balance_label = ttk.Label(info_frame, text=f"${self.players[0].tokens}")
        self.balance_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Game message
        self.message_label = ttk.Label(main_frame, text="Welcome to Poker!")
        self.message_label.pack(pady=10)

        # Financial tip
        self.tip_label = ttk.Label(main_frame, text="", wraplength=700)
        self.tip_label.pack(pady=10)

        # Action frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)

        # Bet amount entry
        ttk.Label(action_frame, text="Bet Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.bet_amount = tk.IntVar(value=10)
        ttk.Entry(action_frame, textvariable=self.bet_amount, width=10).grid(row=0, column=1, padx=5, pady=5)

        # Action buttons
        ttk.Button(action_frame, text="Fold", command=self.fold_hand).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(action_frame, text="Call", command=self.call_bet).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(action_frame, text="Raise", command=self.raise_bet).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(action_frame, text="New Hand", command=self.start_new_hand).grid(row=1, column=3, padx=5, pady=5)

    def start_new_hand(self):
        # Reset game state
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 10  # Small blind
        self.round = 0

        # Reset player hands
        for player in self.players:
            player.new_hand()
            player.add_card(self.deck.draw_card())
            player.add_card(self.deck.draw_card())

        # Update GUI
        self.update_gui()
        self.message_label.config(text="New hand started. Your turn!")

    def update_gui(self):
        # Update community cards
        for i in range(5):
            if i < len(self.community_cards):
                self.community_labels[i].config(text=str(self.community_cards[i]))
            else:
                self.community_labels[i].config(text="")

        # Update player cards
        for i in range(2):
            if i < len(self.players[0].cards):
                self.player_labels[i].config(text=str(self.players[0].cards[i]))
            else:
                self.player_labels[i].config(text="")

        # Update game info
        self.pot_label.config(text=f"${self.pot}")
        self.current_bet_label.config(text=f"${self.current_bet}")
        self.balance_label.config(text=f"${self.players[0].tokens}")

    def fold_hand(self):
        if self.networked_game:
            self.network.send_action("fold")
        else:
            self.message_label.config(text="You folded. Hand over.")
            self.end_round()

    def call_bet(self):
        if self.networked_game:
            self.network.send_action("call")
        else:
            amount = self.current_bet
            bet_amount = self.players[0].place_bet(amount)
            self.pot += bet_amount
            self.message_label.config(text=f"You called ${bet_amount}")
            self.progress_game()

    def raise_bet(self):
        amount = self.bet_amount.get()
        if amount <= self.current_bet:
            messagebox.showwarning("Invalid Bet", "Raise amount must be greater than current bet")
            return

        if self.networked_game:
            self.network.send_action(f"raise {amount}")
        else:
            bet_amount = self.players[0].place_bet(amount)
            self.pot += bet_amount
            self.current_bet = amount
            self.message_label.config(text=f"You raised to ${bet_amount}")
            self.progress_game()

    def progress_game(self):
        # AI players take their turns
        for ai_player in self.ai_players:
            # Simple AI logic
            decision = random.choice(["fold", "call", "raise"])
            if decision == "fold":
                self.message_label.config(text=f"{ai_player.name} folded")
            elif decision == "call":
                bet_amount = ai_player.place_bet(self.current_bet)
                self.pot += bet_amount
                self.message_label.config(text=f"{ai_player.name} called ${bet_amount}")
            else:  # raise
                raise_amount = min(self.current_bet * 2, ai_player.tokens)
                bet_amount = ai_player.place_bet(raise_amount)
                self.pot += bet_amount
                self.current_bet = raise_amount
                self.message_label.config(text=f"{ai_player.name} raised to ${bet_amount}")

        # Progress to next round
        self.round += 1
        if self.round == 1:  # Flop
            for _ in range(3):
                self.community_cards.append(self.deck.draw_card())
            self.message_label.config(text="Flop dealt")
        elif self.round == 2:  # Turn
            self.community_cards.append(self.deck.draw_card())
            self.message_label.config(text="Turn dealt")
        elif self.round == 3:  # River
            self.community_cards.append(self.deck.draw_card())
            self.message_label.config(text="River dealt")
        elif self.round >= 4:  # Showdown
            self.end_round()
            return

        # Reset current bet for new round
        self.current_bet = 0
        self.update_gui()

    def end_round(self):
        # Determine winner
        best_rank = -1
        winners = []

        for player in self.players:
            rank = player.evaluate_hand(self.community_cards)
            if rank > best_rank:
                best_rank = rank
                winners = [player]
            elif rank == best_rank:
                winners.append(player)

        # Split pot among winners
        win_amount = self.pot // len(winners)
        for winner in winners:
            winner.win_pot(win_amount)

        # Update message
        if len(winners) == 1:
            self.message_label.config(text=f"{winners[0].name} won ${win_amount}!")
        else:
            winner_names = ", ".join([w.name for w in winners])
            self.message_label.config(text=f"Split pot between {winner_names}, ${win_amount} each")

        # Update GUI
        self.update_gui()

    def handle_server_message(self, message):
        # Process server messages and update GUI
        parts = message.split()
        command = parts[0]

        if command == "community_cards":
            self.community_cards = []
            for i in range(1, len(parts), 2):
                rank = parts[i]
                suit = parts[i + 1]
                self.community_cards.append(Card(rank, suit, f"{rank}_of_{suit}.png"))
        elif command == "your_cards":
            self.players[0].cards = []
            for i in range(1, len(parts), 2):
                rank = parts[i]
                suit = parts[i + 1]
                self.players[0].add_card(Card(rank, suit, f"{rank}_of_{suit}.png"))
        elif command == "pot":
            self.pot = int(parts[1])
        elif command == "bet":
            self.current_bet = int(parts[1])
        elif command == "balance":
            self.players[0].tokens = int(parts[1])
        elif command == "message":
            self.message_label.config(text=" ".join(parts[1:]))
        elif command == "winner":
            winner_name = parts[1]
            amount = int(parts[2])
            self.message_label.config(text=f"{winner_name} won ${amount}!")

        self.update_gui()

    def display_financial_tip(self):
        tip = FinancialTips.get_random_tip()
        self.tip_label.config(text=f"Financial Tip: {tip}")