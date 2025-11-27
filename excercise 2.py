import tkinter as tk
import random

# ------------------------
# Joke list (natural jokes)
# ------------------------
JOKES = [
    "Why don't skeletons fight each other? They don’t have the guts.",
    "I told my computer I needed a break… it said no problem — it needed one too.",
    "Why do bees have sticky hair? Because they use honeycombs.",
    "I tried to catch fog yesterday. Mist.",
    "What do you call a sleeping bull? A bulldozer.",
    "Why don’t eggs tell jokes? They’d crack each other up.",
    "I used to be addicted to the hokey pokey… but I turned myself around.",
]

# ------------------------
# Tkinter App
# ------------------------
root = tk.Tk()
root.title("Alexa - Tell Me a Joke")
root.geometry("500x300")
root.configure(bg="#1e1e2f")   # Dark background

# ------------------------
# Styles
# ------------------------
TITLE_FONT = ("Segoe UI", 20, "bold")
JOKE_FONT = ("Segoe UI", 14)
BTN_FONT = ("Segoe UI", 12, "bold")

# ------------------------
# Functions
# ------------------------
last_joke = None

def tell_joke():
    global last_joke
    choices = [j for j in JOKES if j != last_joke]  # avoid repeat
    joke = random.choice(choices)
    last_joke = joke
    joke_label.config(text=joke)

# ------------------------
# UI Layout
# ------------------------
title = tk.Label(
    root,
    text="Alexa, tell me a joke",
    font=TITLE_FONT,
    fg="white",
    bg="#1e1e2f"
)
title.pack(pady=15)

frame = tk.Frame(root, bg="#2b2f45", bd=2, relief="flat")
frame.pack(pady=10, padx=20, fill="both", expand=True)

joke_label = tk.Label(
    frame,
    text="Press the button to hear a joke!",
    wraplength=450,
    justify="center",
    font=JOKE_FONT,
    fg="#f0f0f0",
    bg="#2b2f45"
)
joke_label.pack(pady=20, padx=10)

btn = tk.Button(
    root,
    text="Tell Me a Joke",
    command=tell_joke,
    font=BTN_FONT,
    bg="#4a5bdc",
    fg="white",
    activebackground="#3c4cc1",
    activeforeground="white",
    width=18,
    height=1,
    relief="flat",
    bd=0
)
btn.pack(pady=10)

root.mainloop()
