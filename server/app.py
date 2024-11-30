from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def home():
    return "Welcome to the Flask Backend!"

@app.route("/upload", methods=["POST"])
def upload_files():
    if "file_0" not in request.files:
        return jsonify({"error": "No files provided"}), 400

    uploaded_files = request.files
    saved_files = []

    for key in uploaded_files:
        file = uploaded_files[key]
        if file.filename == "":
            return jsonify({"error": f"File {key} has no filename"}), 400

        # Save the file to the upload folder
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        saved_files.append(file.filename)

    return jsonify({"message": "Files uploaded successfully", "files": saved_files}), 200

@app.route("/songs", methods=["GET"])
def get_songs():
    try:
        songs = [f for f in os.listdir("./output_mp3") if f.endswith(".wav")]
        return jsonify(songs=songs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/songs/<filename>')
def serve_song(filename):
    return send_from_directory('path_to_your_songs_folder', filename)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
