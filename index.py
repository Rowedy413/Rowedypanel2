from flask import Flask, request, jsonify, send_from_directory
import json, os

app = Flask(__name__)

DATA_FILE = "users.json"

# Load users from file
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    if not all(k in data for k in ("name", "phone", "username", "password")):
        return jsonify({"error": "Missing fields"}), 400
    users = load_users()
    users.append(data)
    save_users(users)
    return jsonify({"status": "success"})

@app.route("/view_users", methods=["POST"])
def view_users():
    data = request.json
    if data.get("admin_password") != "JAI BABA KI":
        return jsonify({"error": "Invalid admin password"}), 403
    return jsonify(load_users())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
