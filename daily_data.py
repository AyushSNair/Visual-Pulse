import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# Create a new SQLite database if it doesn't exist
conn = sqlite3.connect('daily_data.db')
cursor = conn.cursor()

# Create the daily_data table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS daily_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    total_items_sold INTEGER,
                    total_cost REAL,
                    expenditure REAL
                )''')
conn.commit()
conn.close()


# Function to insert today's data into the database using a context manager
def insert_daily_data(total_items_sold, total_cost, expenditure=0):
    today_date = date.today().strftime("%Y-%m-%d")
    query = '''INSERT INTO daily_data (date, total_items_sold, total_cost, expenditure)
               VALUES (?, ?, ?, ?)'''
    with sqlite3.connect('daily_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, (today_date, total_items_sold, total_cost, expenditure))
        conn.commit()


# Function to update values and insert daily data into the database using a context manager
def update_and_store_data():
    global total_expenditure_entry, table_treeview, entry_sold, cost_values

    total_expenditure = total_expenditure_entry.get().strip()
    if total_expenditure:
        update_values(table_treeview, entry_sold, cost_values)  # Update the table values
        total_items_sold = int(table_treeview.item('extra_row', 'values')[2])
        total_cost = float(table_treeview.item('extra_row', 'values')[4])
        expenditure = float(total_expenditure)
        insert_daily_data(total_items_sold, total_cost, expenditure)  # Insert daily data into the database
    else:
        messagebox.showwarning("Missing Data", "Please enter the total expenditure.")


# Define the update_values function to update the table values
def update_values(table_treeview, entry_sold, cost_values):
    total_items_sold = 0
    total_cost = 0
    conn = sqlite3.connect('sales_product.db')
    cursor = conn.cursor()

    for idx, item in enumerate(table_treeview.get_children(), start=1):
        if item != 'extra_row':  # Skip 'extra_row' in the loop
            product_name = table_treeview.item(item, 'values')[1]
            sold_value = entry_sold[item].get()
            cost_value = cost_values[item]
            total_item_cost = int(sold_value) * float(cost_value)  # Calculate total cost for the item
            table_treeview.item(item, values=(idx, product_name, sold_value, cost_value, total_item_cost))
            total_items_sold += int(sold_value)
            total_cost += total_item_cost  # Add the total item cost to the overall total cost

            # Update quantity_now in the database
            cursor.execute("SELECT qty_start FROM sales_product WHERE product_name = ?", (product_name,))
            qty_start = cursor.fetchone()[0]  # Fetch the qty_start value
            new_qty_now = qty_start - int(sold_value)  # Calculate the new qty_now value
            cursor.execute("UPDATE sales_product SET qty_now = ? WHERE product_name = ?",
                           (new_qty_now, product_name))

    # Update the values in the extra row for total items sold and total cost
    table_treeview.item('extra_row', values=('Total', '', total_items_sold, '', total_cost))

    conn.commit()
    conn.close()


def create_gui():
    global total_expenditure_entry, table_treeview, entry_sold, cost_values  # Define global variables

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

    # Connect to SQLite database and fetch product names, cost, and IDs from sales_product table
    conn = sqlite3.connect('sales_product.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sr_no, product_name, cost, qty_start, qty_now FROM sales_product''')
    data = cursor.fetchall()
    conn.close()

    # Populate the table with product names, cost, and initial values for No. of Items Sold and Total Cost
    entry_sold = {}
    cost_values = {}
    for idx, (sr_no, product_name, cost, qty_start, qty_now) in enumerate(data, start=1):
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

    # Add an extra row for total items sold and total cost
    table_treeview.insert('', tk.END, iid='extra_row', values=('Total', '', 0, 0, 0))

    # Button to update values and store data
    update_button = tk.Button(window, text="Update Values and Store Data", command=update_and_store_data)
    update_button.pack()

    table_treeview.pack()

    window.mainloop()


# Call the create_gui function to run the GUI
create_gui()
