from database import init_db, insert_receipt
import sqlite3

# Step 1: initialize DB
init_db()

# Step 2: insert test data
test_data = {
    "store_name": "Walmart",
    "date": "2026-04-03",
    "time": "14:30:00",
    "total_amount": 5.50,
    "transactions": [
        {"item_name": "Milk", "price": 3.50},
        {"item_name": "Bread", "price": 2.00}
    ]
}

insert_receipt(test_data)

# Step 3: check what's inside
conn = sqlite3.connect("receipts.db")
cursor = conn.cursor()

print("\nReceipts:")
for row in cursor.execute("SELECT * FROM receipts"):
    print(row)

print("\nItems:")
for row in cursor.execute("SELECT * FROM items"):
    print(row)

conn.close()