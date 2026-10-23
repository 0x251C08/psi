from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return jsonify({"message": "Welcome to ${project_name}"})


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    return jsonify(data), 201


@app.route('/items/<int:item_id>')
def get_item(item_id):
    return jsonify({"item_id": item_id, "name": f"Item {item_id}"})


if __name__ == '__main__':
    app.run(debug=True)