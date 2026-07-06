from flask import Blueprint, request, jsonify
from data.database import get_db_connection
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id")
    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows]), 200


@auth_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    username = data.get("username")
    role = data.get("role")

    if not username or not role:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, role) VALUES (?, ?)",
            (username, role)
        )

        conn.commit()

        new_id = cursor.lastrowid

        conn.close()

        return jsonify({
            "id": new_id,
            "username": username,
            "role": role
        }), 201

    except sqlite3.IntegrityError as e:
        conn.close()
        print(e)
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        conn.close()
        print(e)
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    username = data.get("username")
    role = data.get("role")

    conn = get_db_connection()
    cursor = conn.cursor()

    if username and role:
        cursor.execute(
            "UPDATE users SET username = ?, role = ? WHERE id = ?",
            (username, role, user_id)
        )

    elif username:
        cursor.execute(
            "UPDATE users SET username = ? WHERE id = ?",
            (username, user_id)
        )

    elif role:
        cursor.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (role, user_id)
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "Usuario actualizado"}), 200


@auth_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Usuario eliminado"}), 200


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return jsonify({
            "message": "Login exitoso",
            "user": dict(row)
        }), 200

    return jsonify({
        "error": "Usuario no encontrado"
    }), 404
