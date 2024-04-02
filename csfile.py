import csv
import sqlite3

def fetch_data_from_database(database_file, table_name):
    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

def monitor_database_changes(database_file, table_name, csv_filename):
    # Fetch initial data from the database
    data = fetch_data_from_database(database_file, table_name)

    # Write initial data to CSV file
    write_to_csv(data, csv_filename)

    # Continuously monitor database changes
    while True:
        new_data = fetch_data_from_database(database_file, table_name)
        if new_data != data:
            # If data has changed, update CSV file
            write_to_csv(new_data, csv_filename)
            print(f'CSV file "{csv_filename}" has been updated successfully.')
            data = new_data

# Specify the path to your SQLite database file
database_file = 'daily_data.db'

# Specify the table name in the database
table_name = 'daily_data'

# Specify the filename for the CSV file
csv_filename = 'output.csv'

# Monitor database changes and update CSV file accordingly
monitor_database_changes(database_file, table_name, csv_filename)
