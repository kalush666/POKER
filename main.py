import tkinter as tk
from tkinter import messagebox
from mysql_integration import sign_up, login

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_button = tk.Button(root, text="Sign Up", command=self.sign_up)
        self.signup_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login(username, password):
            main()
        else:
            messagebox.showerror("Login", "Invalid credentials")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        sign_up(username, password)
        messagebox.showinfo("Sign Up", "Sign up successful")

def main():
    root = tk.Tk()
    game = PokerGame(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()