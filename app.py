import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

app = Flask(__name__)

# ---- MySQL Config (read from env vars or fallback) ----
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'flaskuser')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'StrongPass123')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flaskdb')

mysql = MySQL(app)

def init_db():
    """Create table if it doesn't exist"""
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            );
        """)
        mysql.connection.commit()
        cur.close()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT message FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_msg = request.form.get('new_message')
    if not new_msg:
        return jsonify({'error': 'Empty message'}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (message) VALUES (%s)", (new_msg,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_msg})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
