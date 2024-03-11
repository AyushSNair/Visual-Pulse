
import sqlite3
import tkinter as tk
#from PIL import Image, ImageTk

def submit_daily_value():
    value = entry.get()

    # Use the 'with' statement to ensure proper connection management
    with sqlite3.connect("expenditurebox") as conn:
        cursor = conn.cursor()
        # cursor.execute('CREATE TABLE IF NOT EXISTS value_entry(value INTEGER (10,5))')
        cursor.execute("insert into value_entry(value) values (?)", (value,))

    display_message.set(f"Hello! Today's expenditure is: {value}")
    # You can add more functionality here

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
title_label = tk.Label(frame, text="Daily expenditure  Box", font=("Helvetica", 16, "bold"), bg="white", fg="#1f2c4b")
title_label.grid(row=0, column=0, pady=10)

# Create an entry box
entry_label = tk.Label(frame, text="Enter expenditure for today:", font=("Arial", 12), bg="white", fg="#1f2c4b")
entry_label.grid(row=1, column=0, pady=10)
entry = tk.Entry(frame, font=("Arial", 12))
entry.grid(row=2, column=0, pady=10)

# Create a submit button and center it
submit_button = tk.Button(frame, text="Submit", command=submit_daily_value, bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
submit_button.grid(row=3, column=0, pady=20)

# Create a message display area
display_message = tk.StringVar()
message_label = tk.Label(frame, textvariable=display_message, font=("Arial", 12, "italic"), bg="white", fg="#1f2c4b")
message_label.grid(row=4, column=0, pady=20)

# Run the Tkinter event loop
window.mainloop()
