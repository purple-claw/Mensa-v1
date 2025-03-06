import os
from b2sdk.v2 import InMemoryAccountinfo, B2Api
from dotenv import load_dotenv

load_dotenv()

B2_APPLICATION_KEY_ID = os.getenv("B2_APPLICATION_KEY_ID")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")

info  = InMemoryAccountinfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY)

bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

def uploadFile2B2(file_path, file_name):
    try:
        with open(file_name, "rb") as file:
            bucket.upload_byted(file.read(), file_name)
        return f"File '{file_name}' Uploaded Sucessfully"
    except Exception as e:
        return f"Error Uploading File: {str(e)}"

def downloadFilefromB2(file_name, save_path):
    try:
        file_version = bucket.get_file_info_by_name(file_name)
        with open(save_path, "wb") as file:
            file.write(file_version.download().read())
        return f"File '{file_name}' downloaded Sucessfully"
    except Exception as e:
        return f"Error Downlaoding file : {str(e)}"
        