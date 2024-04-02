import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# Define global variables
total_expenditure_entry = None
table_treeview = None
entry_sold = {}
cost_values = {}
window = None
holiday_var = None
season_var = None

# Create a new SQLite database if it doesn't exist
conn = sqlite3.connect('daily_data.db')
cursor = conn.cursor()

# Create the daily_data table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS daily_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    total_items_sold INTEGER,
                    total_cost REAL,
                    expenditure REAL,
                    holiday TEXT,
                    season TEXT
                )''')
conn.commit()
conn.close()

# Function to insert today's data into the database using a context manager
def insert_daily_data(total_items_sold, total_cost, expenditure=0, holiday=None, season=None):
    today_date = date.today().strftime("%Y-%m-%d")
    query = '''INSERT INTO daily_data (date, total_items_sold, total_cost, expenditure, holiday, season)
               VALUES (?, ?, ?, ?, ?, ?)'''
    with sqlite3.connect('daily_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, (today_date, total_items_sold, total_cost, expenditure, holiday, season))
        conn.commit()

# Function to update values and insert daily data into the database using a context manager
def update_and_store_data():
    global total_expenditure_entry, table_treeview, entry_sold, cost_values, holiday_var, season_var

    total_expenditure = total_expenditure_entry.get().strip()
    if total_expenditure:
        # Update the table values directly
        # Example: Assume updating the 'No. of Items Sold' and 'Total Cost' based on user input
        total_items_sold = 0
        total_cost = 0
        for item_id, entry_widget in entry_sold.items():
            items_sold = int(entry_widget.get())
            cost = float(cost_values[item_id])
            total_cost += items_sold * cost
            total_items_sold += items_sold
        table_treeview.insert('', tk.END, values=(None, 'Total', total_items_sold, '', total_cost))

        expenditure = float(total_expenditure)
        holiday = holiday_var.get()
        season = season_var.get()
        insert_daily_data(total_items_sold, total_cost, expenditure, holiday, season)  # Insert daily data into the database
        messagebox.showinfo("Success", "Data has been successfully stored in the database.")  # Show success message
    else:
        messagebox.showwarning("Missing Data", "Please enter the total expenditure.")

# Function to fetch data from the database and populate the GUI
# Function to fetch data from the database and populate the GUI
def fetch_data_and_populate_gui():
    global table_treeview, entry_sold, cost_values

    # Connect to SQLite database and fetch product names, cost, and IDs from daily_data table
    conn = sqlite3.connect('daily_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, product_name, cost FROM sales_product''')
    data = cursor.fetchall()
    conn.close()

    # Populate the table with product names, cost, and initial values for No. of Items Sold and Total Cost
    for idx, (sr_no, product_name, cost) in enumerate(data, start=1):
        item_id = table_treeview.insert('', tk.END, values=(
            idx, product_name, 0, cost, 0))  # Assuming initial values for No. of Items Sold and Total Cost are 0

        # Label for Product Name
        product_label = tk.Label(window, text=product_name)
        product_label.pack()

        # Label for No. of Items Sold
        sold_label = tk.Label(window, text='No. of Items Sold:')
        sold_label.pack()
        entry_sold[item_id] = tk.Entry(window)
        entry_sold[item_id].pack()

        # Label for Cost
        cost_label = tk.Label(window, text='Cost:')
        cost_label.pack()

        # Display cost value from database without allowing user input
        cost_value_label = tk.Label(window, text=cost)
        cost_value_label.pack()
        cost_values[item_id] = cost  # Store cost value for calculations

# Function to create the GUI
def create_gui():
    global total_expenditure_entry, table_treeview, entry_sold, cost_values, window, holiday_var, season_var  # Define global variables

    # Create the main window
    window = tk.Tk()
    window.title("DAILY DATA")

    # Label for Daily Data and Date
    daily_data_label = tk.Label(window, text="DAILY DATA", font=('Arial', 18, 'bold'))
    daily_data_label.pack(anchor='n')

    today_date = date.today().strftime("%Y-%m-%d")
    date_label = tk.Label(window, text="Today's Date: " + today_date, font=('Arial', 10))
    date_label.pack(anchor='n')

    # Label for Total Expenditure above the table
    total_expenditure_label = tk.Label(window, text="Total Expenditure:", font=('Arial', 12, 'bold'))
    total_expenditure_label.pack(anchor='w')

    # Entry for user input of total expenditure
    total_expenditure_entry = tk.Entry(window)
    total_expenditure_entry.pack(anchor='w')

    # Dropdown menu for Holiday
    holiday_label = tk.Label(window, text="Holiday:")
    holiday_label.pack(anchor='w')
    holiday_var = tk.StringVar(window)
    holiday_var.set("No")  # Default value
    holiday_dropdown = ttk.Combobox(window, textvariable=holiday_var, values=["Yes", "No"])
    holiday_dropdown.pack(anchor='w')

    # Dropdown menu for Season
    season_label = tk.Label(window, text="Season:")
    season_label.pack(anchor='w')
    season_var = tk.StringVar(window)
    season_var.set("Summer")  # Default value
    season_dropdown = ttk.Combobox(window, textvariable=season_var,
                                   values=["Summer", "Winter", "Autumn", "Spring", "Monsoon"])
    season_dropdown.pack(anchor='w')

    # Subheading for Sales per Product
    subheading_label = tk.Label(window, text="Sales per Product", font=('Arial', 14, 'bold'))
    subheading_label.pack(anchor='w', pady=10)

    # Treeview to display data in tabular form with editable cells
    table_treeview = ttk.Treeview(window, columns=('Sr. No', 'Product', 'No. of Items Sold', 'Cost', 'Total Cost'),
                                  show='headings', height=5)
    table_treeview.heading('Sr. No', text='Sr. No')
    table_treeview.heading('Product', text='Product')
    table_treeview.heading('No. of Items Sold', text='No. of Items Sold')
    table_treeview.heading('Cost', text='Cost')
    table_treeview.heading('Total Cost', text='Total Cost')

    # Call the function to fetch data and populate the GUI
    fetch_data_and_populate_gui()

    # Button to update values and store data
    update_button = tk.Button(window, text="Update Values and Store Data", command=update_and_store_data)
    update_button.pack()

    table_treeview.pack()

    window.mainloop()


# Call the create_gui function to run the GUI
create_gui()
