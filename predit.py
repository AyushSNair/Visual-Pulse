import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load data
data = pd.read_csv("sales_data.csv")

# Handle categorical data
features = data[["Previous_Sale", "Season"]]
target = data["Week Sale"]
nfeatures = pd.get_dummies(features)

# Model
model = LinearRegression()
model.fit(nfeatures.values, target)

# Sample actual previous sales data (replace this with your actual data)
actual_previous_sales = [12, 15, 20, 18]

# GUI function
def predict_sales():
    season_map = {"Winter": 1, "Spring": 2, "Summer": 3, "Autumn": 4}
    selected_season = season_combobox.get()
    selected_previous_sale = float(previous_sale_entry.get())

    try:
        season_code = season_map[selected_season]
    except KeyError:
        messagebox.showerror("Error", "Invalid season selected.")
        return

    if selected_previous_sale not in [1, 2, 3, 4]:
        messagebox.showerror("Error", "Invalid previous sale input.")
        return

    # Predict sales for each unique value of previous sale
    predicted_sales = []
    for prev_sale in [1, 2, 3, 4]:
        if prev_sale == 1:
            d = [[season_code, 1, 0, 0, 0]]
        elif prev_sale == 2:
            d = [[season_code, 0, 1, 0, 0]]
        elif prev_sale == 3:
            d = [[season_code, 0, 0, 1, 0]]
        else:
            d = [[season_code, 0, 0, 0, 1]]
        predicted_price = model.predict(d)[0]
        predicted_sales.append(predicted_price * 10 * 7)

    # Plot graph
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], actual_previous_sales, label='Actual Previous Sales', color='blue')
    ax.plot([1, 2, 3, 4], predicted_sales, label='Predicted Sales', color='red')
    ax.set_xlabel('Previous Sale')
    ax.set_ylabel('Sales')
    ax.set_title('Comparison of Actual Previous Sales and Predicted Sales')
    ax.set_xticks([1, 2, 3, 4])  # Set x-axis ticks to integer values
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create main window
root = tk.Tk()
root.title("Sales Prediction")

# Season selection
season_label = tk.Label(root, text="Select Season:")
season_label.grid(row=0, column=0, padx=10, pady=5)
season_combobox = ttk.Combobox(root, values=["Winter", "Spring", "Summer", "Autumn"])
season_combobox.grid(row=0, column=1, padx=10, pady=5)
season_combobox.current(0)

# Previous sale input
previous_sale_label = tk.Label(root, text="Enter Previous Year's Sale (1, 2, 3, 4):")
previous_sale_label.grid(row=1, column=0, padx=10, pady=5)
previous_sale_entry = ttk.Entry(root)
previous_sale_entry.grid(row=1, column=1, padx=10, pady=5)

# Predict button
predict_button = tk.Button(root, text="Predict Sales", command=predict_sales)
predict_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Frame for graph
graph_frame = tk.Frame(root)
graph_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
