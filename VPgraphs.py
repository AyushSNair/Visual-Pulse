import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter.messagebox import *
from sqlite3 import *

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
inc = []

def submit_daily_value():
    con = None
    try:
        con = connect("entry1.db")
        cursor = con.cursor()
        for entry in inc:
            val = int(entry.get())  # Convert the value to an integer
            sql = "INSERT INTO entry1 (val) VALUES (?)"
            cursor.execute(sql, (val,))
        con.commit()
        showinfo("Success", "Values entered successfully!")
    except Exception as e:
        con.rollback()
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()

    plot_data()

def plot_data():
    plt.plot(days, [int(entry.get()) for entry in inc], marker="o")
    plt.legend(["income"], loc=2)
    plt.grid(color="grey", linewidth=1)
    plt.xlabel("Days")
    plt.ylabel("Income")
    plt.title("Weekly Business Analysis")

    total_income = sum([int(entry.get()) for entry in inc])
    average_income = total_income / 6

    if average_income >= 5000:
        profit = int(average_income - 5000)
        profit_message = f"You have a profit of {profit} rupees.\nKeep it up!"
        plt.text(0.5, 0.9, profit_message, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center', bbox=dict(facecolor='green', alpha=0.5))
    else:
        loss = int(5000 - average_income)
        loss_message = f"You have a loss of {loss} rupees.\nConsider these suggestions\n1.Review and analyze all expenses to identify where costs can be reduced without compromising quality.\n2.Implement innovative solutions to stay competitive in the market."
        plt.text(0.5, 0.9, loss_message, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center', bbox=dict(facecolor='red', alpha=0.5))

    plt.show()

# Create the main window
window = tk.Tk()
window.title("Daily Input Box")
window.configure(bg="#1f2c4b",width=500,height=500)

# Create a frame with a white background and subtle border
frame = tk.Frame(window, bg="white", padx=60, pady=60, bd=5, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title_label = tk.Label(frame, text="Daily Input Box", font=("Helvetica", 16, "bold"), bg="white", fg="#1f2c4b")
title_label.grid(row=0, column=0, pady=10)

# Create entry boxes dynamically
for i in range(6):
    entry_label = tk.Label(frame, text=f"Enter value for {days[i]}:", font=("Arial", 12), bg="white", fg="#1f2c4b")
    entry_label.grid(row=2*i+1, column=0, pady=10)
    n = tk.Entry(frame, font=("Arial", 12))
    n.grid(row=2*i+2, column=0, pady=10)
    inc.append(n)

# Create a submit button and center it
submit_button = tk.Button(frame, text="Submit", command=submit_daily_value, bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
submit_button.grid(row=13, column=0, pady=20)

# Create a message display area
display_message = tk.StringVar()
message_label = tk.Label(frame, textvariable=display_message, font=("Arial", 12, "italic"), bg="white", fg="#1f2c4b")
message_label.grid(row=14, column=0, pady=20)

window.mainloop()
