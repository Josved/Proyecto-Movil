# routes/orders.py
from flask import Blueprint, request, jsonify
from data.database import get_db_connection

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    table_number = data.get('table_number')
    items = data.get('items')
    
    if not table_number or not items:
        return jsonify({"error": "Faltan datos de la orden"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total = sum(item['quantity'] * item['price'] for item in items)
    
    cursor.execute("INSERT INTO orders (table_number, status, total) VALUES (?, 'Pendiente', ?)", (table_number, total))
    order_id = cursor.lastrowid
    
    for item in items:
        cursor.execute('''
            INSERT INTO order_items (order_id, product_name, quantity, price) 
            VALUES (?, ?, ?, ?)
        ''', (order_id, item['product_name'], item['quantity'], item['price']))
        
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Orden creada por el mesero", "order_id": order_id, "total": total}), 201

@orders_bp.route('/api/orders/kitchen', methods=['GET'])
def get_kitchen_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE status IN ('Pendiente', 'En Cocina')")
    rows = cursor.fetchall()
    
    orders = [dict(row) for row in rows]
    
    for order in orders:
        cursor.execute("SELECT product_name, quantity FROM order_items WHERE order_id = ?", (order['id'],))
        order['items'] = [dict(item) for item in cursor.fetchall()]
        
    conn.close()
    return jsonify(orders), 200

@orders_bp.route('/api/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({"error": "Falta el nuevo estado"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Orden actualizada a: {new_status}"}), 200

@orders_bp.route('/api/orders/table/<int:table_number>', methods=['GET'])
def get_table_bill(table_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE table_number = ? AND status != 'Pagado' ORDER BY id DESC LIMIT 1", (table_number,))
    order_row = cursor.fetchone()
    
    if not order_row:
        conn.close()
        return jsonify({"error": "No hay cuentas activas para esta mesa"}), 404
        
    order = dict(order_row)
    cursor.execute("SELECT product_name, quantity, price FROM order_items WHERE order_id = ?", (order['id'],))
    order['items'] = [dict(item) for item in cursor.fetchall()]
    conn.close()
    
    return jsonify(order), 200