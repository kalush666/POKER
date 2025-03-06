import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from Deck import Deck
from Player import Player
from FinancialTips import FinancialTips
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql_integration


class PokerGame:
    def __init__(self, root, user_data=None):
        self.root = root
        self.root.title("Poker Game with Financial Tips")
        self.root.geometry("1000x700")

        self.user_data = user_data
        self.deck = Deck()
        self.current_player_index = 0
        self.pot = 0
        self.round = 0  # 0: pre-flop, 1: flop, 2: turn, 3: river
        self.community_cards = []
        self.card_images = []
        self.min_bet = 10
        self.current_bet = 0
        self.session_start_time = datetime.datetime.now()

        self.setup_players()
        self.create_ui()
        self.show_financial_tip()

    def setup_players(self):
        # Initialize with AI opponents
        initial_balance = 1000
        if self.user_data:
            initial_balance = float(self.user_data['balance'])

        self.players = [
            Player("You", initial_balance),
            Player("AI Player 1", 1000),
            Player("AI Player 2", 1000)
        ]

        self.starting_balances = {player.name: player.tokens for player in self.players}

    def create_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create game area
        self.game_frame = ttk.Frame(self.main_frame)
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create sidebar for stats and tips
        self.sidebar_frame = ttk.Frame(self.main_frame, width=300)
        self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for the game
        self.canvas = tk.Canvas(self.game_frame, width=700, height=600, bg="darkgreen")
        self.canvas.pack(pady=10)

        # Load and display the background image if available
        try:
            image_path = os.path.join(os.path.dirname(__file__), "table.jpg")
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((700, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)
        except:
            # If image can't be loaded, just use the green background
            print("Background image couldn't be loaded, using green background")

        # Game control buttons
        self.control_frame = ttk.Frame(self.game_frame)
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.deal_button = ttk.Button(self.control_frame, text="Deal New Hand", command=self.start_game)
        self.deal_button.pack(side=tk.LEFT, padx=5)

        self.bet_frame = ttk.Frame(self.control_frame)
        self.bet_frame.pack(side=tk.LEFT, padx=5)

        self.bet_amount = tk.StringVar(value=str(self.min_bet))
        self.bet_spinner = ttk.Spinbox(self.bet_frame, from_=self.min_bet, to=9999, textvariable=self.bet_amount,
                                       width=5)
        self.bet_spinner.pack(side=tk.LEFT)

        self.raise_button = ttk.Button(self.control_frame, text="Raise", command=self.raise_bet)
        self.raise_button.pack(side=tk.LEFT, padx=5)

        self.call_button = ttk.Button(self.control_frame, text="Call", command=self.call_bet)
        self.call_button.pack(side=tk.LEFT, padx=5)

        self.check_button = ttk.Button(self.control_frame, text="Check", command=self.check_bet)
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.fold_button = ttk.Button(self.control_frame, text="Fold", command=self.fold_hand)
        self.fold_button.pack(side=tk.LEFT, padx=5)

        # Initially disable action buttons
        self.toggle_action_buttons(False)

        # Status label
        self.status_label = ttk.Label(self.game_frame, text="Welcome to Poker Game with Financial Tips!")
        self.status_label.pack(pady=5)

        # Set up the sidebar content
        self.setup_sidebar()

    def setup_sidebar(self):
        # Title for the sidebar
        sidebar_title = ttk.Label(self.sidebar_frame, text="Financial Dashboard", font=("Arial", 14, "bold"))
        sidebar_title.pack(pady=10)

        # Player balance frame
        balance_frame = ttk.LabelFrame(self.sidebar_frame, text="Your Balance")
        balance_frame.pack(fill=tk.X, padx=10, pady=5)

        self.balance_var = tk.StringVar(value=f"${self.players[0].tokens:.2f}")
        balance_label = ttk.Label(balance_frame, textvariable=self.balance_var, font=("Arial", 12))
        balance_label.pack(pady=5)

        # Session stats frame
        stats_frame = ttk.LabelFrame(self.sidebar_frame, text="Session Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        # Profit/Loss
        self.profit_loss_var = tk.StringVar(value="Profit/Loss: $0.00")
        profit_loss_label = ttk.Label(stats_frame, textvariable=self.profit_loss_var)
        profit_loss_label.pack(anchor=tk.W, pady=2)

        # Hands played
        self.hands_played_var = tk.StringVar(value="Hands played: 0")
        hands_played_label = ttk.Label(stats_frame, textvariable=self.hands_played_var)
        hands_played_label.pack(anchor=tk.W, pady=2)

        # Win rate
        self.win_rate_var = tk.StringVar(value="Win rate: 0%")
        win_rate_label = ttk.Label(stats_frame, textvariable=self.win_rate_var)
        win_rate_label.pack(anchor=tk.W, pady=2)

        # Financial tips frame
        tips_frame = ttk.LabelFrame(self.sidebar_frame, text="Financial Tip of the Day")
        tips_frame.pack(fill=tk.X, padx=10, pady=5)

        self.tip_var = tk.StringVar(value="Click 'New Tip' for financial advice")
        tip_label = ttk.Label(tips_frame, textvariable=self.tip_var, wraplength=280, justify=tk.LEFT)
        tip_label.pack(pady=5, fill=tk.X)

        tip_button = ttk.Button(tips_frame, text="New Tip", command=self.show_financial_tip)
        tip_button.pack(pady=5)

        # Financial goals frame
        goals_frame = ttk.LabelFrame(self.sidebar_frame, text="Financial Goals")
        goals_frame.pack(fill=tk.X, padx=10, pady=5)

        self.goals_var = tk.StringVar(value="No financial goals set")
        goals_label = ttk.Label(goals_frame, textvariable=self.goals_var, wraplength=280, justify=tk.LEFT)
        goals_label.pack(pady=5, fill=tk.X)

        goals_button = ttk.Button(goals_frame, text="Set New Goal", command=self.set_financial_goal)
        goals_button.pack(pady=5)

        # Save session button
        save_button = ttk.Button(self.sidebar_frame, text="Save Session Stats", command=self.save_session)
        save_button.pack(pady=10)

        # Add small performance chart at the bottom of sidebar
        self.chart_frame = ttk.Frame(self.sidebar_frame)
        self.chart_frame.pack(fill=tk.X, padx=10, pady=10)

        self.create_performance_chart()

    def create_performance_chart(self):
        # Clear previous chart if it exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Create a simple balance chart
        fig, ax = plt.subplots(figsize=(3, 2))

        # We'll use player history data if it exists, otherwise use dummy data
        balances = [self.starting_balances.get(self.players[0].name, 1000)]
        session_data = [self.players[0].tokens]

        ax.plot(["Start", "Current"], balances + session_data, marker='o')
        ax.set_title("Balance Trend")
        ax.set_ylabel("Balance ($)")
        ax.grid(True, alpha=0.3)

        # Add profit/loss data
        profit_loss = session_data[0] - balances[0]
        color = "green" if profit_loss >= 0 else "red"
        ax.text(1, session_data[0], f"{profit_loss:+.2f}", color=color)

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_financial_tip(self):
        self.tip_var.set(FinancialTips.get_random_tip())

    def set_financial_goal(self):
        if not self.user_data:
            messagebox.showinfo("Login Required", "Please log in to set financial goals.")
            return

        goal_name = simpledialog.askstring("Financial Goal", "What are you saving for?")
        if not goal_name:
            return

        try:
            target_amount = float(simpledialog.askstring("Target Amount", "How much do you need? ($)"))
            if target_amount <= 0:
                messagebox.showwarning("Invalid Amount", "Please enter a positive amount.")
                return
        except (ValueError, TypeError):
            messagebox.showwarning("Invalid Amount", "Please enter a valid number.")
            return

        # Optional target date
        date_str = simpledialog.askstring("Target Date (Optional)",
                                          "When do you want to reach this goal? (YYYY-MM-DD or leave blank)")
        target_date = None
        if date_str:
            try:
                target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please use YYYY-MM-DD format or leave blank.")
                return

        # Create the goal in database
        success = mysql_integration.create_financial_goal(
            self.user_data['id'], goal_name, target_amount, target_date
        )

        if success:
            date_info = f" by {target_date}" if target_date else ""
            self.goals_var.set(f"Goal: {goal_name}\nTarget: ${target_amount:.2f}{date_info}")
            messagebox.showinfo("Success", "Financial goal created successfully!")
        else:
            messagebox.showerror("Error", "Could not create financial goal.")

    def save_session(self):
        if not self.user_data:
            messagebox.showinfo("Login Required", "Please log in to save your session stats.")
            return

        player = self.players[0]
        starting_balance = self.starting_balances.get(player.name, 1000)
        ending_balance = player.tokens
        hands_played = player.stats["hands_played"]
        hands_won = player.stats["hands_won"]

        # Update user balance in database
        balance_updated = mysql_integration.update_balance(self.user_data['id'], ending_balance)

        # Save session statistics
        session_saved = mysql_integration.save_game_session(
            self.user_data['id'],
            starting_balance,
            ending_balance,
            hands_played,
            hands_won
        )

        if balance_updated and session_saved:
            messagebox.showinfo("Success", "Session data saved successfully!")

            # Update the user_data with new balance
            self.user_data['balance'] = ending_balance
        else:
            messagebox.showerror("Error", "Could not save session data.")

        # Refresh chart
        self.create_performance_chart()

    def update_stats_display(self):
        player = self.players[0]  # Main player

        # Update balance
        self.balance_var.set(f"${player.tokens:.2f}")

        # Calculate profit/loss
        starting_balance = self.starting_balances.get(player.name, 1000)
        profit_loss = player.tokens - starting_balance
        sign = "+" if profit_loss >= 0 else ""
        self.profit_loss_var.set(f"Profit/Loss: {sign}${profit_loss:.2f}")

        # Update hands played
        self.hands_played_var.set(f"Hands played: {player.stats['hands_played']}")

        # Calculate win rate
        win_rate = 0
        if player.stats["hands_played"] > 0:
            win_rate = (player.stats["hands_won"] / player.stats["hands_played"]) * 100
        self.win_rate_var.set(f"Win rate: {win_rate:.1f}%")

        # Update chart
        self.create_performance_chart()

    def toggle_action_buttons(self, enabled=True):
        state = "normal" if enabled else "disabled"
        self.raise_button["state"] = state
        self.call_button["state"] = state
        self.check_button["state"] = state
        self.fold_button["state"] = state

    def start_game(self):
        self.pot = 0
        self.round = 0
        self.current_bet = 0
        self.community_cards = []

        self.deck = Deck()  # New shuffled deck

        # Deal cards to players
        for player in self.players:
            player.new_hand()
            for _ in range(2):
                player.add_card(self.deck.draw_card())

        # Collect small and big blind
        self.collect_blinds()

        # Enable action buttons
        self.toggle_action_buttons(True)

        # Update display
        self.display_game_state()
        self.update_stats_display()

        # Show a tip when starting a new hand
        if random.random() < 0.3:  # 30% chance
            self.show_financial_tip()

    def collect_blinds(self):
        small_blind = self.min_bet // 2
        big_blind = self.min_bet

        # Collect small blind from player 1
        sb_player = self.players[1]
        sb_bet = sb_player.place_bet(small_blind)
        self.pot += sb_bet

        # Collect big blind from player 2
        bb_player = self.players[2]
        bb_bet = bb_player.place_bet(big_blind)
        self.pot += bb_bet

        self.current_bet = big_blind
        self.status_label.config(text=f"Small blind: {small_blind}, Big blind: {big_blind}")

    def display_game_state(self):
        self.canvas.delete("all")

        # Draw background
        if hasattr(self, 'bg_photo'):
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)
        else:
            self.canvas.config(bg="darkgreen")

        self.card_images = []  # Clear previous card images

        # Show community cards
        self.display_community_cards()

        # Show player cards
        self.display_player_cards()

        # Show pot
        self.canvas.create_text(350, 200, text)