from flask import Blueprint, request, jsonify
from utils.b2_storage import uploadFile2B2, getFileUrl
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

b2_routes = Blueprint("b2_routes", __name__)

@b2_routes.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({
            "error": "No file Provided"
        }), 400
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(file_path)

    response = uploadFile2B2(file_path, file.filename)
    os.remove(file_path)
    return jsonify({
        "Message" : response
    })

@b2_routes.route("/get-file-url", methods=["GET"])
def get_file():
    file_name = request.args.get("filename")
    
    if not file_name:
        return jsonify({"error": "Filename is required"}), 400

    file_url = getFileUrl(file_name)

    return jsonify({"file_url": file_url})