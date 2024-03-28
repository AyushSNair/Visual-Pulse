from sqlite3 import *
from tkinter.messagebox import *



#
# #statements to fire required query into the databse tables
#
# print("Enter your income")
# r = input()
#
# query = "insert into value_entry(value) values (" + r + ")"
#
# con.execute(query)
# con.commit()
#
# con.close()
#



import tkinter as tk
#from PIL import Image, ImageTk

def submit_daily_value():
    con = None
    try:
        con = connect("entry.db")
        cursor = con.cursor()
        val = int(entry.get())  # Convert the value to an integer
        sql = "INSERT INTO entry (val) VALUES (?)"
        cursor.execute(sql, (val,))
        con.commit()
        showinfo("Success", "Value entered successfully!")
    except Exception as e:
        con.rollback()
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()

    # You can add more functionality here

# Create the main window
window = tk.Tk()
window.title("Daily Input Box")

# Set the background color of the main window to dark blue
window.configure(bg="#1f2c4b",width=500,height=500)

# Load the transparent background image
#image = Image.open("transparent_background.png")
#background_image = ImageTk.PhotoImage(image)

# Create a frame with a white background and subtle border
frame = tk.Frame(window, bg="white", padx=60, pady=60, bd=5, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Set the image as the background of the frame
#background_label = tk.Label(frame, image=background_image)
#background_label.place(relwidth=1, relheight=1)

# Title
title_label = tk.Label(frame, text="Daily Input Box", font=("Helvetica", 16, "bold"), bg="white", fg="#1f2c4b")
title_label.grid(row=0, column=0, pady=10)

# Create an entry box
#1
entry_label = tk.Label(frame, text="Enter value for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=1, column=0, pady=10)
n = entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=2, column=0, pady=10)

#2
entry_label = tk.Label(frame, text="Enter value for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=3, column=0, pady=10)
n = entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=4, column=0, pady=10)

#3
entry_label = tk.Label(frame, text="Enter value for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=5, column=0, pady=10)
n = entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=6, column=0, pady=10)

#4
entry_label = tk.Label(frame, text="Enter value for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=7, column=0, pady=10)
n = entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=8, column=0, pady=10)
#5
entry_label = tk.Label(frame, text="Enter value for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=9, column=0, pady=10)
n = entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=10, column=0, pady=10)

#6
entry_label = tk.Label(frame, text="Enter value for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=11, column=0, pady=10)
n = entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=12, column=0, pady=10)

# Create a submit button and center it
submit_button = tk.Button(frame, text="Submit", command=submit_daily_value, bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
submit_button.grid(row=13, column=0, pady=20)

# Create a message display area
display_message = tk.StringVar()
message_label = tk.Label(frame, textvariable=display_message, font=("Arial", 12, "italic"), bg="white", fg="#1f2c4b")
message_label.grid(row=4, column=0, pady=20)

# Run the Tkinter event loop
window.mainloop()