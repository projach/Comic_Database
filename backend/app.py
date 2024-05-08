from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('comics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS comics (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        volume TEXT,
                        box TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to insert a comic into the database
def insert_comic(title, volume, box):
    conn = sqlite3.connect('comics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comics WHERE title=? AND volume=? AND box=?', (title, volume, box))
    duplicate = cursor.fetchone()
    if duplicate:
        conn.close()
        return jsonify({'message': 'Comic already exists'}), 400
    else:
        cursor.execute('INSERT INTO comics (title, volume, box) VALUES (?, ?, ?)', (title, volume, box))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Comic inserted successfully'}), 200

# Function to fetch all comics from the database
def fetch_comics():
    conn = sqlite3.connect('comics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comics ORDER BY title')
    rows = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'title': row[1], 'volume': row[2], 'box': row[3]} for row in rows]

def search_comics(search):
    conn = sqlite3.connect('comics.db')
    cursor = conn.cursor()
    # Pass the search term as a tuple with a single element
    cursor.execute('SELECT * FROM comics WHERE title LIKE ? ORDER BY title', ('%' + search + '%',))
    rows = cursor.fetchall()
    conn.close()
    # Return a list of dictionaries containing the result
    return [{'id': row[0], 'title': row[1], 'volume': row[2], 'box': row[3]} for row in rows]

# Function to delete a comic from the database
def delete_comic_sql(comic_id):
    conn = sqlite3.connect('comics.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comics WHERE id=?', (comic_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute('DELETE FROM comics WHERE id=?', (comic_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Comic deleted successfully'}), 200
    else:
        conn.close()
        return jsonify({'message': 'Comic not found'}), 404

# Endpoint to handle POST requests for uploading comics
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    title = data.get('title')
    volume = data.get('volume')
    box = data.get('box')
    return insert_comic(title, volume, box)

# Endpoint to handle GET requests for fetching comics
@app.route('/comics', methods=['GET'])
def get_comics():
    search_query = request.args.get('search')
    if search_query is not None:
        comics = search_comics(search_query)
    else:
        comics = fetch_comics()
    return jsonify(comics), 200

@app.route('/delete-comic', methods=['POST'])
def delete_comic():
    return delete_comic_sql(request.get_json().get('id'))

# Initialize the database when the application starts
initialize_database()

if __name__ == '__main__':
    app.run(debug=True)