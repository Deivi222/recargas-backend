from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

USERS_FILE = "users.json"

def load_users():
    """Carga los usuarios desde el archivo"""
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Guarda los usuarios en el archivo"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def find_user(users, user_id):
    """Busca un usuario en la lista"""
    for user in users:
        if user["user_id"] == user_id:
            return user
    return None

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "Backend activo y funcionando"
    })

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"status": "error", "message": "user_id requerido"}), 400

    user_id = data["user_id"]
    users = load_users()

    user = find_user(users, user_id)
    if not user:
        users.append({"user_id": user_id, "status": "pendiente"})
        save_users(users)

    return jsonify({"status": "ok", "message": "Usuario registrado", "user_id": user_id})

@app.route("/check_user", methods=["POST"])
def check_user():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"status": "error", "message": "user_id requerido"}), 400

    user_id = data["user_id"]
    users = load_users()
    user = find_user(users, user_id)

    authorized = user is not None and user["status"] == "aprobado"

    return jsonify({"status": "ok", "user_id": user_id, "authorized": authorized})

@app.route("/aprobar", methods=["POST"])
def aprobar():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"status": "error", "message": "user_id requerido"}), 400

    user_id = data["user_id"]
    users = load_users()
    user = find_user(users, user_id)

    if user:
        user["status"] = "aprobado"
        save_users(users)
        return jsonify({"status": "ok", "message": "Usuario aprobado", "user_id": user_id})
    else:
        return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

@app.route("/rechazar", methods=["POST"])
def rechazar():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"status": "error", "message": "user_id requerido"}), 400

    user_id = data["user_id"]
    users = load_users()
    user = find_user(users, user_id)

    if user:
        user["status"] = "rechazado"
        save_users(users)
        return jsonify({"status": "ok", "message": "Usuario rechazado", "user_id": user_id})
    else:
        return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Bot-Hosting asigna el puerto
    app.run(host="0.0.0.0", port=port)
