import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('wallet_app.db')
cursor = conn.cursor()

# Add a new column 'phone' to the 'transactions' table
cursor.execute('ALTER TABLE transactions ADD COLUMN phone TEXT')

# Commit the changes and close the connection
conn.commit()
conn.close()
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('wallet_app.db')
cursor = conn.cursor()

# Set the phone number and wallet ID values
phone_number = '7019834252'
wallet_id = 1

# Update the 'phone' column for rows with wallet_id = 1
cursor.execute('UPDATE transactions SET phone = ? WHERE wallet_id = ?', (phone_number, wallet_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
