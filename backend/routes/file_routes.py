from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.b2_storage import uploadFile2B2, getFileUrl, generateSignedUrl
from database import files_collection
import os
import datetime

file_bp = Blueprint("file", __name__)

@file_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    curr_usr = get_jwt_identity()
    if "file" not in request.files:
        return jsonify({"error": "File Not Provided"}), 400
    file = request.files["file"]
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    upload_response = uploadFile2B2(file_path, file.filename)
    signed_url = generateSignedUrl(file.filename)
    os.remove(file_path)

    if "Error" in upload_response:
        return jsonify({"error": upload_response}), 500

    file_url = getFileUrl(file.filename)
    if "Error" in file_url:
        return jsonify({"error": file_url}), 500

    file_info = {
        "filename": file.filename,
        "uploaded_by": curr_usr,
        "uploaded_at": datetime.datetime.utcnow(),
        "b2_url": signed_url
    }
    files_collection.insert_one(file_info)
    return jsonify({"message": "File uploaded", "file_url": signed_url}), 200