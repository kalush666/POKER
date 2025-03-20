import tkinter as tk
from tkinter import messagebox
from MySql import sign_up, login, create_players_table
from PokerGame import PokerGame


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Game Login")
        self.root.geometry("300x200")

        # Create database tables if they don't exist
        create_players_table()

        # Username field
        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack(pady=(20, 0))
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=(5, 10))

        # Password field
        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=(5, 10))

        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Login button
        self.login_button = tk.Button(button_frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5)

        # Sign up button
        self.signup_button = tk.Button(button_frame, text="Sign Up", command=self.sign_up)
        self.signup_button.grid(row=0, column=1, padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return

        if login(username, password):
            self.root.destroy()  # Close login window
            self.start_game(username)
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Sign Up Error", "Please enter both username and password")
            return

        try:
            sign_up(username, password)
            messagebox.showinfo("Sign Up", "Registration successful! You can now login.")
        except Exception as e:
            messagebox.showerror("Sign Up Error", f"Failed to register: {str(e)}")

    def start_game(self, username):
        game_root = tk.Tk()
        game = PokerGame(game_root, {"username": username})
        game_root.mainloop()


def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()