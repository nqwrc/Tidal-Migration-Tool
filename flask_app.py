from flask import Flask, render_template, jsonify, request
import tidalapi
from tidal_migrator import TidalMigrator
from pathlib import Path

app = Flask(__name__)
migrator = TidalMigrator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    return jsonify(url=migrator.url_main)

@app.route('/check_login', methods=['GET'])
def check_login():
    if migrator.check_login():
        return jsonify(status="Logged in"), 200
    else:
        return jsonify(status="Not logged in"), 401
    
@app.route('/post_login_content')
def post_login_content():
    return render_template('post_login.html')

@app.route('/add_favorites', methods=['POST'])
def add_favorites_route():
    filepaths = request.json.get('filepaths')
    errors = migrator.add_favorites([Path(fp) for fp in filepaths])
    if errors:
        return jsonify(errors=errors), 400
    return jsonify(message="Favorites added successfully"), 200

@app.route('/save_favorites', methods=['GET'])
def save_favorites_route():
    migrator.save_favorites()
    return jsonify(message="Favorites saved successfully"), 200

@app.route('/get_favorites')
def get_favorites():
    try:
        favorites = migrator.get_favorites()
        return jsonify(favorites)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
