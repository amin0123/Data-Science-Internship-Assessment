from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    id = data.get('id')
    
    if id > 5:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, id) VALUES (?, ?)", (name, id))
            conn.commit()
    
    users_above_5 = get_users_above_5()
    return jsonify({'names_with_ids_above_5': users_above_5})

def get_users_above_5():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE id > 5")
        rows = cursor.fetchall()
        return [row[0] for row in rows]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
