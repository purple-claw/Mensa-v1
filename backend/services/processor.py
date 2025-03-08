import requests
import json
import os
from datetime import datetime
from database import processed_data_collection

def fetch_and_process_data(api_url, output_format='json'):
    response = requests.get(api_url)
    raw_data = response.json()

    if isinstance(raw_data, list):
        # Handle the case where raw_data is a list
        processed_data = []
        for item in raw_data:
            processed_data.append(process_item(item))
        usage_info = process_and_save_data(processed_data, output_format)
        return usage_info
    elif isinstance(raw_data, dict):
        # Handle the case where raw_data is a dictionary
        processed_data = process_item(raw_data)
        usage_info = process_and_save_data([processed_data], output_format)
        return usage_info
    else:
        return {"error": "Unexpected data format"}

def process_item(item):
    # Process the item and return the result
    return {
        "market": item.get("market"),
        "korean_name": item.get("korean_name"),
        "english_name": item.get("english_name")
    }

def process_and_save_data(data, output_format='json'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'processed_data_{timestamp}.{output_format}'

    if output_format == 'json':
        processed_data_json = json.dumps(data, indent=4)
        save_to_mongodb(processed_data_json, filename)

    usage_info = {
        "description": "Processed data from API.",
        "usage": "The file contains all the data fetched from the API.",
        "timestamp": timestamp,
        "file": filename
    }

    # Save usage information to MongoDB
    save_to_mongodb(usage_info, f'usage_info_{timestamp}')

    return usage_info

def save_to_mongodb(data, filename):
    document = {
        "filename": filename,
        "data": data,
        "timestamp": datetime.now()
    }
    processed_data_collection.insert_one(document)

def fetch_and_store_data(output_filename=None):
    # Fetch data from MongoDB
    data = list(processed_data_collection.find({}, {"_id": 0}))

    # Generate a timestamp for the filename if not provided
    if not output_filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'processed_data_{timestamp}.json'

    # Define the output file path
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'processed_data')
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, output_filename)

    # Write data to the JSON file
    with open(output_filepath, 'w') as output_file:
        json.dump(data, output_file, indent=4)

    return output_filepath
