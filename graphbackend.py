import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('graph_data.db')
cursor = conn.cursor()

# Retrieve data from the database
cursor.execute('''SELECT title, x_data, y_data FROM graphs''')
graphs = cursor.fetchall()

# Plot each retrieved graph
for graph in graphs:
    title, x_data, y_data = graph
    x_values = x_data.split(',')
    y_values = [int(y) for y in y_data.split(',')]

    plt.plot(x_values, y_values, marker="o")
    plt.xlabel("Days")
    plt.ylabel("Income")
    plt.title(title)
    plt.show()

# Close the database connection
conn.close()
