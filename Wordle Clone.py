import tkinter as tk
import random
from tkinter import messagebox

class WordleClone:
    def __init__(self, master):
        self.master = master
        master.title("Wordle Clone")

        self.word_list = [
            "ABOUT", "ABOVE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADORE", "ADULT", "AFTER", "AGAIN",
            "AGENT", "AGREE", "AHEAD", "AISLE", "ALBUM", "ALERT", "ALIEN", "ALIKE", "ALIVE", "ALLOW",
            "ALONE", "ALONG", "ALTER", "AMONG", "ANGER", "ANGLE", "ANGRY", "ANODE", "ANTIC", "APART",
            "APPLY", "ARENA", "ARGUE", "ARISE", "ARMY", "AROUND", "ARRIVE", "ARROW", "ASIDE", "ASSET",
            "AUNT", "AVOID", "AWAKE", "AWARD", "AWARE", "AWFUL", "BADLY", "BAKER", "BALKY", "BASIC",
            "BASIS", "BATON", "BEACH", "BEGAN", "BEGIN", "BEING", "BELOW", "BENCH", "BENDY", "BESET",
            "BESTOW", "BETEL", "BETRAY", "BETTER", "BEVEL", "BEWARE", "BEYOND", "BIOME", "BLAME",
            "BLAST", "BLAZE", "BLEAK", "BLEND", "BLIND", "BLISS", "BLOCK", "BLOOM", "BLOWN", "BLUER",
            "BLUFF", "BLUNT", "BLURB", "BLURT", "BOARD", "BOAST", "BOGGY", "BOOST", "BORAX", "BORER",
            "BORING", "BORROW", "BOSOM", "BOSSY", "BOTCH", "BOULE", "BOUND", "BOWEL", "BOXER", "BRAID",
            "BRAIN", "BRAKE", "BRAND", "BRASH", "BRASS", "BRAVE", "BRAWL", "BRAWNY", "BRAYER", "BREAD",
            "BREAK"
        ]
        self.secret_word = random.choice(self.word_list)
        self.attempts = 0
        self.max_attempts = 6
        self.guess_entries = []

        for i in range(self.max_attempts):
            row_entries = []
            for j in range(5):
                entry = tk.Entry(master, width=3, font=("Arial", 24), justify="center", state="disabled")
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.guess_entries.append(row_entries)

        self.current_guess_row = 0
        self.active_guess_entry = 0
        self.enable_current_row()

        self.master.bind("<Key>", self.handle_key_press)
        self.master.bind("<Return>", self.submit_guess)

        self.feedback_label = tk.Label(master, text="", font=("Arial", 14))
        self.feedback_label.grid(row=self.max_attempts + 1, column=0, columnspan=5, pady=10)

    def enable_current_row(self):
        for entry in self.guess_entries[self.current_guess_row]:
            entry.config(state="normal")
        if self.guess_entries[self.current_guess_row]:
            self.guess_entries[self.current_guess_row][0].focus_set()
            self.active_guess_entry = 0

    def disable_current_row(self):
        for entry in self.guess_entries[self.current_guess_row]:
            entry.config(state="disabled")

    def handle_key_press(self, event):
        if 'a' <= event.char.lower() <= 'z':
            row = self.guess_entries[self.current_guess_row]
            if self.active_guess_entry < 5:
                row[self.active_guess_entry].delete(0, tk.END)
                row[self.active_guess_entry].insert(0, event.char.upper())
                self.active_guess_entry += 1
                if self.active_guess_entry < 5:
                    row[self.active_guess_entry].focus_set()
        elif event.keysym == 'BackSpace':
            row = self.guess_entries[self.current_guess_row]
            if self.active_guess_entry > 0:
                self.active_guess_entry -= 1
                row[self.active_guess_entry].delete(0, tk.END)
                row[self.active_guess_entry].focus_set()

    def submit_guess(self, event=None):
        row = self.guess_entries[self.current_guess_row]
        guess = "".join([entry.get() for entry in row]).upper()
        if len(guess) == 5 and guess in [word.upper() for word in self.word_list]:
            self.check_guess(guess)
        elif len(guess) != 5:
            self.feedback_label.config(text="Guess must be 5 letters long.")
        elif guess not in [word.upper() for word in self.word_list]:
            self.feedback_label.config(text="Not a valid word.")

    def check_guess(self, guess):
        secret = self.secret_word
        feedback_colors = ["gray"] * 5
        temp_secret = list(secret)
        row = self.guess_entries[self.current_guess_row]

        # Check for correct letters in the correct position (green)
        for i in range(5):
            if guess[i] == secret[i]:
                feedback_colors[i] = "green"
                temp_secret[i] = ""  # Mark as used

        # Check for correct letters in the wrong position (yellow)
        for i in range(5):
            if feedback_colors[i] != "green" and guess[i] in temp_secret:
                feedback_colors[i] = "yellow"
                temp_secret[temp_secret.index(guess[i])] = "" # Mark as used

        for i, color in enumerate(feedback_colors):
            row[i].config(bg=color)

        self.current_guess_row += 1
        self.active_guess_entry = 0

        if guess == secret:
            self.feedback_label.config(text=f"You guessed it! The word was {secret}")
            self.disable_all_entries()
        elif self.attempts < self.max_attempts - 1:
            self.enable_current_row()
        else:
            self.feedback_label.config(text=f"You ran out of attempts! The word was {secret}")
            self.disable_all_entries()

        self.attempts += 1

    def disable_all_entries(self):
        for row in self.guess_entries:
            for entry in row:
                entry.config(state="disabled")
        self.master.unbind("<Key>")
        self.master.unbind("<Return>")

root = tk.Tk()
game = WordleClone(root)
root.mainloop()