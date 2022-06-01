from flask import Flask, g, render_template, request
import sqlite3

# Create web app, run with flask run
app = Flask(__name__)

# Create main page
@app.route('/')
def main():
    return render_template('main.html')

#submit page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            # call the database function if successful submission
            message, handle = insert_message()
            return render_template('submit.html', thanks=True, message=message, handle=handle)
        except:
            return render_template('submit.html', error=True)

def get_message_db():
    """
    1. Check whether there is a database called message_db in the g attribute of the app. If not, then connect to that database.
    2. Check whether a table called messages exists in message_db.
    3. Return the connection g.message_db
    """
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        # Check whether a table called messages exists in message_db
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            handle TEXT NOT NULL)
        """
        cursor = g.message_db.cursor()

        #execute the command
        cursor.execute(cmd)

        # return the connection g.message_db.
        return g.message_db

def insert_message():
    """
    1.Extract the message and the handle from request. 
    2.Using a cursor, insert the message into the message database.
    """
    conn = get_message_db()

    # use request.form to get data when submitting a form with the POST method.
    cmd = \
    f"""
    INSERT INTO messages (message, handle) 
    VALUES ("{request.form["message"]}", "{request.form["handle"]}")
    """
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()

    # close the database connection
    conn.close()
    return request.form["message"], request.form["handle"]

@app.route('/view/')
def view(): 
    return render_template('view.html', messages=random_messages(5))
    
def random_messages(n):
    """
    1. call the funtion get_message_db()
    2. random select the data from database
    """
    db = get_message_db()
    r_m = db.execute(f"SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}").fetchall()

    # close the database connection
    db.close()
    return r_m