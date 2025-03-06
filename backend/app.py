from flask import Flask, request, jsonify
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/", methods=["GET"])

def home():
    return jsonify({
        "Message" : "Backend is Running!",
        "API" : Config.API_URL,
        "debug_mode" : True
    })

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({
            "error": "No file Provided"
        }), 400
    file = request.files["file"]
    file_path = os.path.join("temp", file.filename)

    file.save(file_path)

    response = uploadFile2B2(file_path, file.filename)
    os.remove(file_path)
    return jsonify({
        "Message" : response
    })


if __name__ == "__main__":
    app.run(debug=True)