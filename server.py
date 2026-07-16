# Activate flask in terminal: .\venv\Scripts\activate
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Root (/) route
# It renders and displays the index.html form template. Silly
@app.route("/")
def home():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM cashgames")
    games = cur.fetchall()
    con.close()
    # render index.html & our query.
    return render_template("index.html", games=games)

# Returns a JSON of the database when button is clicked
@app.route("/button-clicked")
def button_clicked():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM cashgames")
    games = cur.fetchall()
    con.close()
    return {
        "message": "Database JSON layout--",
        "games.db": games
    }

# This bad boy renders the пост запросы (post requests) when form is submitted.
# It captures the input and makes a new row and inputs column data
@app.route("/read-form", methods=["POST"])
def read_form():
    fgame = request.form.get("userGame")
    freward = request.form.get("reward")
    fstatus = request.form.get("status")  
    # Does this really return extracted from data as JSON response?
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    # Form data being parsed into sql
    sql = f'''INSERT INTO cashgames(offer, reward, status) 
              VALUES ("{fgame}", "{freward}", "{fstatus}")'''
    cur.execute(sql)
    con.commit()
    cur.execute("SELECT * FROM cashgames")
    games = cur.fetchall()
    con.close()
    return render_template("index.html", games=games)

# Deletes row using dropdown
@app.route("/delete-row", methods=["POST"])
def delete_row():
    rowID = request.form.get("rowID")
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cashgames WHERE id = ?", (rowID,))
    con.commit()
    cur.execute("SELECT * FROM cashgames")
    games = cur.fetchall()
    con.close()
    return render_template("index.html", games=games)

# Deletes row using button
@app.route("/delete-button", methods=["POST"])
def delete_button():
    buttonID = request.form.get("buttonID")
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cashgames WHERE id = ?", (buttonID,))
    con.commit()
    cur.execute("SELECT * FROM cashgames")
    games = cur.fetchall()
    con.close()
    return render_template("index.html", games=games)
    # return {
    #     "message": f"deleted row with button id {buttonID}",
    # }    
        
# Enables debug modes
app.run(host="0.0.0.0", debug=True)