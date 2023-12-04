import sqlite3

# Connect to the database (or create it if it doesn't exist)
# conn = sqlite3.connect("wallet_app.db")
# cursor = conn.cursor()
#
# # Create add_account table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS add_account (
#         account_number INTEGER PRIMARY KEY,
#         fullname TEXT NOT NULL,
#         account_holder_name TEXT NOT NULL,
#         account_type TEXT NOT NULL,
#         bank_name TEXT NOT NULL,
#         branch_name TEXT NOT NULL,
#         ifsc_code TEXT NOT NULL
#     )
# ''')

# Create add_money table with foreign key reference to add_account



# Connect to the SQLite database
conn = sqlite3.connect("wallet_app.db")
cursor = conn.cursor()

# Execute SQL statements
try:
    # Alter the add_money table
    # cursor.execute("ALTER TABLE add_money RENAME TO old_add_money1")

    # Create a new add_money table with the updated attributes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS add_money (
            wallet_id TEXT PRIMARY KEY,
            currency_type TEXT DEFAULT 'INR',
            balance REAL DEFAULT 0,
            e_money REAL DEFAULT 0,
            phone_no TEXT(10) REFERENCES signup(phone_no),
            account_number INTEGER REFERENCES add_account(account_number),
            bank_name TEXT DEFAULT NULL
        )
    ''')

    # Insert dummy values into the new add_money table
    cursor.executemany('''
        INSERT INTO add_money (wallet_id, currency_type, balance, e_money, phone_no, account_number, bank_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        ('dummy1', 'USD', 1000, 50, '1234567890', 1, 'BankA'),
        ('dummy2', 'EUR', 500, 25, '9876543210', 2, 'BankB'),
        ('dummy3', 'JPY', 200, 10, '5555555555', 3, None),
    ])

    # Commit the changes
    conn.commit()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    # Close the connection
    conn.close()



# Insert dummy values into add_account table
# cursor.execute('''
#     INSERT INTO add_account (fullname, account_holder_name, account_type, bankname, branch_name, ifsc_code)
#     VALUES
#         ('John Doe', 'John Doe', 'Savings', 'ABC Bank', 'Main Branch', 'ABC1234567'),
#         ('Jane Doe', 'Jane Doe', 'Checking', 'XYZ Bank', 'Downtown Branch', 'XYZ9876543')
# ''')
#
# # Insert dummy values into add_money table
# cursor.execute('''
#     INSERT INTO add_money (account_number, e_money)
#     VALUES
#         (1, 1000.50),
#         (2, 500.75)
# ''')
#
# # Commit the changes and close the connection
# conn.commit()
# conn.close()
#
# # Display the data
# conn = sqlite3.connect("wallet_app.db")
# cursor = conn.cursor()
#
# # Display add_account table
# cursor.execute('''
#     SELECT * FROM add_account
# ''')
# print("add_account Table:")
# for row in cursor.fetchall():
#     print(row)
#
# # Display add_money table
# cursor.execute('''
#     SELECT * FROM add_money
# ''')
# print("\nadd_money Table:")
# for row in cursor.fetchall():
#     print(row)
#
# # Close the connection
# conn.close()