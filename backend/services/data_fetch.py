import json
import os
from datetime import datetime
from database import processed_data_collection

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
