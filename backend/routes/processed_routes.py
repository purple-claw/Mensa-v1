from flask import Blueprint, request, jsonify
from services.processor import fetch_and_process_data, fetch_and_store_data

processed_bp = Blueprint("processed", __name__)

@processed_bp.route("/process_data", methods=["POST"])
def fetch_and_process():
    data = request.json
    api_url = data.get("api_url")
    output_format = data.get("output_format", "json")

    if not api_url:
        return jsonify({"error": "API URL is required"}), 400

    result = fetch_and_process_data(api_url, output_format)
    return jsonify(result)

@processed_bp.route("/fetch_data", methods=["GET"])
def fetch_stored_data():
    output_filename = request.args.get("output_filename")
    output_filepath = fetch_and_store_data(output_filename)
    return jsonify({"message": "Data stored successfully", "file_path": output_filepath})