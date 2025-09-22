from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))
PASSWORD = os.getenv("PASSWORD", "")

entries = []

@dataclass
class Entry:
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    happiness: str = ""

@app.route("/")
def index():
    return render_template("index.html", entries=entries)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password", "")
        if not PASSWORD:
            flash("PASSWORD ist nicht konfiguriert (.env / App Settings).", "error")
            return redirect(url_for("login"))
        if pw == PASSWORD:
            session["logged_in"] = True
            flash("Login erfolgreich.", "success")
            return redirect(url_for("index"))
        flash("Falsches Passwort.", "error")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logout erfolgreich.", "success")
    return redirect(url_for("index"))

@app.route("/add_entry", methods=["POST"])
def add_entry():
    content = request.form.get("content", "").strip()
    happiness = request.form.get("happiness", "").strip()
    if content:
        entries.append(Entry(content=content, happiness=happiness))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)