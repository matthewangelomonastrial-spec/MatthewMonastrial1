from tkinter import *
import random

root = Tk()
root.title('Math Quiz')
root.geometry('450x350')
root.config(bg='#1e1e2f')  # Dark background

score = 0
question_count = 0

# --- Functions ---
def new_question():
    global num1, num2, operation, question_count
    question_count += 1
    if question_count > 10:
        end_quiz()
        return

    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(["+", "-"])

    if operation == "+":
        question_label.config(text=f"{num1} + {num2} = ?")
    else:
        question_label.config(text=f"{num1} - {num2} = ?")

    answer_entry.delete(0, END)
    feedback_label.config(text="")

def check_answer():
    global score
    try:
        user_answer = int(answer_entry.get())
        correct_answer = num1 + num2 if operation == "+" else num1 - num2

        if user_answer == correct_answer:
            score += 1
            feedback_label.config(text="✅ Correct!", fg="#00ffcc")
        else:
            feedback_label.config(text=f"❌ Wrong! Correct: {correct_answer}", fg="#ff6b6b")

        score_label.config(text=f"Score: {score}")
        root.after(1000, new_question)
    except ValueError:
        feedback_label.config(text="Please enter a number!", fg="#ffcc00")

def end_quiz():
    question_label.config(text=f"Quiz Finished! 🎉")
    answer_entry.pack_forget()
    submit_btn.pack_forget()
    feedback_label.config(text=f"Your final score: {score}/10", fg="#00ffcc")

# --- Heading ---
title_label = Label(root, text="🧮 Math Quiz 🧮",
                    bg='#1e1e2f', fg="#f0f0f0",
                    font=("Helvetica", 18, "bold"))
title_label.pack(pady=20)

# --- Question Label ---
question_label = Label(root, text="Press Start to Begin!",
                       bg='#1e1e2f', fg="#00ffcc",
                       font=("Helvetica", 16))
question_label.pack(pady=10)

# --- Answer Entry ---
answer_entry = Entry(root, font=("Helvetica", 14), width=10, justify='center')
answer_entry.pack(pady=10)

# --- Submit Button ---
submit_btn = Button(root, text="Submit", command=check_answer,
                    fg="#1e1e2f", bg="#00ffcc",
                    font=("Helvetica", 12, "bold"), width=10)
submit_btn.pack(pady=10)

# --- Feedback Label ---
feedback_label = Label(root, text="", bg='#1e1e2f', fg="#ff6b6b", font=("Helvetica", 12))
feedback_label.pack(pady=10)

# --- Score Label ---
score_label = Label(root, text="Score: 0", bg='#1e1e2f', fg="#f0f0f0", font=("Helvetica", 12))
score_label.pack(pady=10)

# --- Start Button ---
start_btn = Button(root, text="Start Quiz", command=new_question,
                   fg="#1e1e2f", bg="#ffaa00",
                   font=("Helvetica", 12, "bold"), width=10)
start_btn.pack(pady=10)

root.mainloop()
