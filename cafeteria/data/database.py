# data/database.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'cafeteria.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL CHECK(role IN ('Administrador', 'Mesero', 'Cocina', 'Caja'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendiente' CHECK(status IN ('Pendiente', 'En Cocina', 'Listo', 'Pagado')),
            total REAL NOT NULL DEFAULT 0.0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)", [
            ("gerente1", "Administrador"),
            ("gerente2", "Administrador"),
            ("mesero_juan", "Mesero"),
            ("mesero_maria", "Mesero"),
            ("mesero_pedro", "Mesero"),
            ("chef_luis", "Cocina"),
            ("chef_carlos", "Cocina"),
            ("cajera_ana", "Caja"),
            ("cajera_sofia", "Caja")
        ])
        
        orders_data = [
            (3, 'Pendiente', 145.00),
            (7, 'Listo', 110.00),
            (1, 'En Cocina', 235.00),
            (4, 'Pagado', 95.00),
            (2, 'Pagado', 320.00),
            (5, 'Pagado', 150.00),
            (8, 'Pagado', 180.00),
            (6, 'Pagado', 85.00)
        ]
        
        items_data = [
            (1, "Café Americano", 2, 45.00),
            (1, "Muffin de Chocolate", 1, 55.00),
            (2, "Capuccino", 1, 55.00),
            (2, "Rebanada de Pastel", 1, 55.00),
            (3, "Bagel de Pollo", 2, 85.00),
            (3, "Frappé de Oreo", 1, 65.00),
            (4, "Espresso Doble", 1, 50.00),
            (4, "Croissant", 1, 45.00),
            (5, "Panini de Tres Quesos", 2, 90.00),
            (5, "Frappé de Oreo", 2, 65.00),
            (5, "Te Verde Ice", 1, 50.00),
            (6, "Capuccino", 2, 55.00),
            (6, "Muffin de Chocolate", 1, 40.00),
            (7, "Bagel de Pollo", 1, 85.00),
            (7, "Café Americano", 1, 45.00),
            (7, "Croissant", 1, 50.00),
            (8, "Rebanada de Pastel", 1, 55.00),
            (8, "Espresso Doble", 1, 30.00)
        ]

        for table, status, total in orders_data:
            cursor.execute("INSERT INTO orders (table_number, status, total) VALUES (?, ?, ?)", (table, status, total))
            
        for order_id, prod_name, qty, price in items_data:
            cursor.execute("INSERT INTO order_items (order_id, product_name, quantity, price) VALUES (?, ?, ?, ?)", (order_id, prod_name, qty, price))

    conn.commit()
    conn.close()
    print("¡Base de datos inicializada con éxito y datos robustos cargados!")

init_db()