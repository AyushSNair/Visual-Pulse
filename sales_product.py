import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def create_gui():
    window = tk.Tk()
    window.title("SALES PRODUCT")
    window.geometry("1650x800")

    conn = sqlite3.connect('sales_product.db')  # Connect to SQLite database
    cursor = conn.cursor()

    # Create the sales_product table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales_product (
                        sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT UNIQUE,
                        cost REAL,
                        qty_start INTEGER,
                        qty_now INTEGER
                    )''')
    conn.commit()

    # Function to insert a new row into the table
    def insert_row():
        product_name = product_name_entry.get().strip()  # Remove leading/trailing spaces
        if not product_name:
            messagebox.showwarning("Add Row", "Product name cannot be empty.")
            return

        try:
            cost_val = float(cost_entry.get())
            qty_start_val = int(qty_start_entry.get())
            qty_now_val = qty_now_entry.get()  # Get the value from entry or set it to None if empty
            if qty_now_val:
                qty_now_val = int(qty_now_val)  # Convert to int if not empty
        except ValueError:
            messagebox.showwarning("Add Row", "Cost and Quantity Start must be numeric.")
            return

        try:
            cursor.execute('''INSERT INTO sales_product (product_name, cost, qty_start, qty_now)
                            VALUES (?, ?, ?, ?)''', (product_name, cost_val, qty_start_val, qty_now_val))
            conn.commit()
            display_data()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Add Row", "Product name already exists.")

    # Function to delete a row by product name
    def delete_row():
        product_name = product_name_entry.get().strip()  # Remove leading/trailing spaces
        if not product_name:
            messagebox.showwarning("Delete Row", "Product name cannot be empty.")
            return

        cursor.execute('''DELETE FROM sales_product WHERE product_name = ?''', (product_name,))
        conn.commit()
        display_data()

    # Function to update a row by product name
    def update_row():
        product_name = product_name_entry.get().strip()  # Remove leading/trailing spaces
        if not product_name:
            messagebox.showwarning("Update Row", "Product name cannot be empty.")
            return

        try:
            cost_val = float(cost_entry.get())
            qty_start_val = int(qty_start_entry.get())
            qty_now_val = qty_now_entry.get()  # Get the value from entry or set it to None if empty
            if qty_now_val:
                qty_now_val = int(qty_now_val)  # Convert to int if not empty
        except ValueError:
            messagebox.showwarning("Update Row", "Cost and Quantity Start must be numeric.")
            return

        cursor.execute('''UPDATE sales_product SET cost = ?, qty_start = ?, qty_now = ?
                        WHERE product_name = ?''', (cost_val, qty_start_val, qty_now_val, product_name))
        conn.commit()
        display_data()

    # Function to display data in the table
    def display_data():
        for row in table_treeview.get_children():
            table_treeview.delete(row)

        cursor.execute('''SELECT * FROM sales_product''')
        data = cursor.fetchall()

        for row in data:
            table_treeview.insert('', tk.END, values=row)

    # Entry fields for adding/updating new data
    product_name_label = tk.Label(window, text="Product Name:", font=('Arial', 12))
    product_name_label.pack()
    product_name_entry = tk.Entry(window, font=('Arial', 12))
    product_name_entry.pack()

    cost_label = tk.Label(window, text="Cost:", font=('Arial', 12))
    cost_label.pack()
    cost_entry = tk.Entry(window, font=('Arial', 12))
    cost_entry.pack()

    qty_start_label = tk.Label(window, text="Quantity Start:", font=('Arial', 12))
    qty_start_label.pack()
    qty_start_entry = tk.Entry(window, font=('Arial', 12))
    qty_start_entry.pack()


    button_row = tk.Frame(window)
    button_row.pack()

    add_button = tk.Button(button_row, text="Add Row", command=insert_row, font=('Arial', 12), width=15)
    add_button.pack(side=tk.LEFT, padx=5)

    update_button = tk.Button(button_row, text="Update Row", command=update_row, font=('Arial', 12), width=15)
    update_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_row, text="Delete Row", command=delete_row, font=('Arial', 12), width=15)
    delete_button.pack(side=tk.LEFT, padx=5)

    # Treeview to display data in tabular form
    table_treeview = ttk.Treeview(window, columns=('Sr. No.', 'Product Name', 'Cost', 'Quantity Start', 'Quantity Now'),
                                  show='headings')
    table_treeview.heading('Sr. No.', text='Sr. No.')
    table_treeview.heading('Product Name', text='Product Name')
    table_treeview.heading('Cost', text='Cost')
    table_treeview.heading('Quantity Start', text='Quantity Start')
    table_treeview.heading('Quantity Now', text='Quantity Now')
    table_treeview.pack()

    display_data()  # Display initial data

    window.mainloop()

# Call the create_gui function to run the GUI
create_gui()
