from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Welcome to the Flask Backend!"


@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        return jsonify({"message": "This is a GET request!", "data": None})
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({"message": "This is a POST request!", "received_data": data})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
