import tkinter as tk
from tkinter import *
import requests
import math

run = True
wpm = 0
acc = 0
BACKGROUND = "#5B8FB9"


# function that calculates words per minute
def word_per():
    global wpm, story_short, acc
    string = entry.get().split()
    words_done = story_short[:len(string)]
    errors = 0
    for i in range(len(words_done)):
        if string[i] != words_done[i]:
            errors += 1
    characters = (len("".join(string)))
    wpm = (((characters / 5) - errors) / 0.083)
    if wpm < 0:
        wpm = 0
    if characters > 0:
        acc = ((characters - errors) / characters) * 100
    word_per_minute.config(text=f"Word Per Minute: {round(wpm, 2)}")
    accuracy.config(text=f"Accuracy: %{round(acc, 2)}")


# start function
def start_command():
    global entry
    entry.config(state="normal")
    start_button.config(state="disabled")
    entry.delete(0, END)
    countdown(10)


def countdown(count):
    global run, wpm
    if run:
        count_minute = math.floor(count / 60)
        count_second = count % 60
        if count_second < 10:
            count_second = f"0{count_second}"

        time = window.after(1000, countdown, count - 1)

        timer_text.config(text=f"{count_minute}:{count_second}")
        # word_per_minute.config(text=f"Word Per Minute: {wpm}")
        word_per()
        if time == "after#10":
            run = False
            entry.config(state="disabled")
            start_button.config(state="normal")
            word_per()
    return


# short story api
url = "https://shortstories-api.onrender.com/"
response = requests.get(url)
story = response.json()
story_split = story['story'].split()
story_short = story_split[:50]

# set up gui to be able to type within a certain amount of time
window = tk.Tk()
window.title('Type Test')
window.geometry("600x500")
window.config(padx=50, pady=50, bg=BACKGROUND)

story_text = Label(window, text=story_short, font="Arial 14", wraplength=500, justify="center", bg=BACKGROUND,
                   fg="white")
story_text.grid(column=1, row=0)

entry = Entry(width=50)
entry.grid(column=1, row=2, pady=20)

start_button = Button(text="Start", command=start_command)
start_button.grid(column=1, row=3)

word_per_minute = Label(text=f"Word Per Minute: {wpm}", font="Arial 14", bg=BACKGROUND, fg="white")
word_per_minute.grid(column=1, row=4)
accuracy = Label(text=f"Accuracy: %{acc}", font="Arial 14", bg=BACKGROUND, fg="white")
accuracy.grid(column=1, row=5)

timer_text = Label(text="0:00", font=("Arial", 35, "bold"), bg=BACKGROUND, fg="white")
timer_text.grid(column=1, row=6)

window.mainloop()
