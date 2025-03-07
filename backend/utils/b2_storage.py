import os
import time
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from dotenv import load_dotenv

load_dotenv()

B2_APPLICATION_KEY_ID = os.getenv("B2_APPLICATION_KEY_ID")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY)

bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

def uploadFile2B2(file_path, file_name):
    try:
        with open(file_path, "rb") as file:
            bucket.upload_bytes(file.read(), file_name)
        return f"File '{file_name}' Uploaded Successfully"
    except Exception as e:
        return f"Error Uploading File: {str(e)}"

def getFileUrl(file_name):
    try:
        file_info = bucket.get_file_info_by_name(file_name)
        download_url = f"https://f005.backblazeb2.com/file/{B2_BUCKET_NAME}/{file_name}"
        return download_url
    except Exception as e:
        return f"Error retrieving file URL: {str(e)}"
    
def generateSignedUrl(file_name, valid_duration=3600):
    try:
        timestamp = int(time.time())
        authorization_token = bucket.get_download_authorization(file_name, valid_duration)
        signed_url = f"https://f005.backblazeb2.com/file/{B2_BUCKET_NAME}/{file_name}?Authorization={authorization_token}"
        return signed_url
    except Exception as e:
        return f"Error generating signed URL: {str(e)}"
    
    