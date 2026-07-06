# routes/stats.py
from flask import Blueprint, jsonify, send_file
import sqlite3
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

stats_bp = Blueprint('stats', __name__)

def get_db_connection():
    conn = sqlite3.connect('data/cafeteria.db')
    conn.row_factory = sqlite3.Row
    return conn

@stats_bp.route('/api/stats/summary', methods=['GET'])
def get_summary():
    conn = get_db_connection()
    total_sales = conn.execute("SELECT SUM(total) FROM orders WHERE status = 'Pagado'").fetchone()[0] or 0.0
    active_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status != 'Pagado'").fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return jsonify({
        "total_sales": total_sales,
        "active_orders": active_orders,
        "total_users": total_users
    }), 200

@stats_bp.route('/api/stats/top-products', methods=['GET'])
def get_top_products():
    conn = get_db_connection()
    # Trae los productos ordenados por cantidad vendida
    query = """
        SELECT product_name, SUM(quantity) as total_qty 
        FROM order_items 
        GROUP BY product_name 
        ORDER BY total_qty DESC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

@stats_bp.route('/api/stats/order-status', methods=['GET'])
def get_order_status():
    conn = get_db_connection()
    rows = conn.execute("SELECT status, COUNT(*) as count FROM orders GROUP BY status").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

# 📊 DESCARGAR EXCEL (.XLSX)
@stats_bp.route('/api/stats/report/excel', methods=['GET'])
def export_excel():
    conn = get_db_connection()
    orders = conn.execute("SELECT id, table_number, total, status FROM orders").fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de Ventas"

    # Encabezados
    ws.append(["ID Orden", "Número de Mesa", "Total ($)", "Estado"])
    for order in orders:
        ws.append([order['id'], order['table_number'], order['total'], order['status']])

    img_box = io.BytesIO()
    wb.save(img_box)
    img_box.seek(0)

    return send_file(img_box, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name="Reporte_Ventas_Cafeteria.xlsx")

# 📄 DESCARGAR PDF
@stats_bp.route('/api/stats/report/pdf', methods=['GET'])
def export_pdf():
    conn = get_db_connection()
    orders = conn.execute("SELECT id, table_number, total, status FROM orders").fetchall()
    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, spaceAfter=20)
    
    elements.append(Paragraph("☕ Reporte General de Ventas y Ganancias", title_style))
    elements.append(Spacer(1, 12))

    # Estructurar Tabla para el PDF
    data = [["ID Orden", "Mesa", "Total ($)", "Estado"]]
    for order in orders:
        data.append([str(order['id']), str(order['table_number']), f"${order['total']:.2f}", order['status']])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name="Reporte_Cafeteria.pdf")