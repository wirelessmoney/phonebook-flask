
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# INIT DB
def init_db():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# HOME
@app.route("/")
def index():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template("index.html", contacts=contacts)

# ADD
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    phone = request.form["phone"]

    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

    return redirect("/")

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# EDIT PAGE
@app.route("/edit/<int:id>")
def edit_page(id):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contacts WHERE id=?", (id,))
    contact = c.fetchone()
    conn.close()

    return render_template("edit.html", contact=contact)

# UPDATE
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"]
    phone = request.form["phone"]

    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, id))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

