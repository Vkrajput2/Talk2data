import sqlite3
import os

DB_NAME = "ecommerce.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        signup_date DATE NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        product_id INTEGER,
        order_date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')
    
    # Check if empty, then seed
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        
    conn.commit()
    conn.close()

def seed_data(cursor):
    customers = [
        ('Alice Smith', 'alice@example.com', '2023-01-15'),
        ('Bob Jones', 'bob@example.com', '2023-03-22'),
        ('Charlie Brown', 'charlie@example.com', '2023-06-10')
    ]
    cursor.executemany('INSERT INTO customers (name, email, signup_date) VALUES (?, ?, ?)', customers)
    
    products = [
        ('Laptop Pro', 'Electronics', 1299.99),
        ('Wireless Mouse', 'Electronics', 49.99),
        ('Coffee Mug', 'Home', 12.50),
        ('Desk Chair', 'Office', 199.00)
    ]
    cursor.executemany('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', products)
    
    orders = [
        (1, 1, '2023-02-01', 1),
        (1, 2, '2023-02-01', 2),
        (2, 4, '2023-04-10', 1),
        (3, 3, '2023-06-15', 4),
        (1, 3, '2023-07-20', 1)
    ]
    cursor.executemany('INSERT INTO orders (customer_id, product_id, order_date, quantity) VALUES (?, ?, ?, ?)', orders)

if __name__ == "__main__":
    init_db()
    print(f"Database {DB_NAME} initialized and seeded.")
