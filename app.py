from flask import Flask, request, jsonify, render_template
import json, os

app = Flask(__name__)

DB_FILE = 'db.json'

def load_db():
    with open(DB_FILE) as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/deposit', methods=['POST'])
def deposit():
    data = request.json
    user = data.get("user_id")
    amount = float(data.get("amount", 0))
    db = load_db()
    if user not in db["users"]:
        db["users"][user] = 0
    db["users"][user] += amount
    db["server_balance"] += amount
    save_db(db)
    return jsonify({"success": True, "balance": db["users"][user]})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    user = data.get("user_id")
    amount = float(data.get("amount", 0))
    db = load_db()
    if user not in db["users"] or db["users"][user] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    db["users"][user] -= amount
    db["server_balance"] -= amount
    save_db(db)
    return jsonify({"success": True, "balance": db["users"][user]})

@app.route('/api/transfer', methods=['POST'])
def transfer():
    data = request.json
    from_user = data.get("from")
    to_user = data.get("to")
    amount = float(data.get("amount", 0))
    db = load_db()
    if from_user not in db["users"] or db["users"][from_user] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    if to_user not in db["users"]:
        db["users"][to_user] = 0
    db["users"][from_user] -= amount
    db["users"][to_user] += amount
    save_db(db)
    return jsonify({"success": True})

@app.route('/api/balance/<user_id>')
def user_balance(user_id):
    db = load_db()
    return jsonify({"balance": db["users"].get(user_id, 0)})

@app.route('/api/server-balance', methods=['POST'])
def server_balance():
    key = os.getenv("ADMIN_SECRET_KEY")
    data = request.json
    if data.get("key") != key:
        return jsonify({"error": "Unauthorized"}), 403
    db = load_db()
    return jsonify({"server_balance": db["server_balance"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
