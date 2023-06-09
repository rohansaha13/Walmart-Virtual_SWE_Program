import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('shipping_data.db')
cursor = conn.cursor()

# Create the necessary tables in the database
cursor.execute('''CREATE TABLE IF NOT EXISTS Spreadsheet0
                (product_id INTEGER PRIMARY KEY,
                 product_name TEXT,
                 quantity INTEGER,
                 origin TEXT,
                 destination TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Spreadsheet1
                (shipping_id INTEGER PRIMARY KEY,
                 product_name TEXT,
                 quantity INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Spreadsheet2
                (shipping_id INTEGER PRIMARY KEY,
                 origin TEXT,
                 destination TEXT)''')

# Insert data from Spreadsheet0
with open('Spreadsheet0.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        cursor.execute('INSERT INTO Spreadsheet0 VALUES (?, ?, ?, ?, ?)', row)

# Insert data from Spreadsheet1
with open('Spreadsheet1.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        shipping_id = int(row[0])
        product_name = row[1]
        quantity = int(row[2])
        
        # Retrieve origin and destination from Spreadsheet2
        cursor.execute('SELECT origin, destination FROM Spreadsheet2 WHERE shipping_id = ?', (shipping_id,))
        result = cursor.fetchone()
        origin = result[0]
        destination = result[1]
        
        # Insert a row for each product in the shipment
        for _ in range(quantity):
            cursor.execute('INSERT INTO Spreadsheet0 (product_name, quantity, origin, destination) VALUES (?, ?, ?, ?)',
                           (product_name, 1, origin, destination))

# Commit the changes and close the connection
conn.commit()
conn.close()
