import base64
import os
import time
from scripts.db.mongo.collections.my_resume import MyResume
from scripts.utils.mongo_utility import mongo_client


def pdf_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        # Read the PDF content
        pdf_content = pdf_file.read()
        # Encode the PDF content to base64
        base64_encoded = base64.b64encode(pdf_content).decode("utf-8")
    return base64_encoded

# Example usage:
pdf_file_path = os.path.join(os.getcwd(), "code", "data", "Tarun_s_CV_new8.pdf") # Replace with your PDF file path
base64_string = pdf_to_base64(pdf_file_path)
data = {
    "last_updated_at": int(time.time()),
    "pdf_data": base64_string,
    "last_fetched_date": int(time.time()),
    "last_fetched_by": "Admin",
    "resume_name": "my_base_resume"
}
MyResume(mongo_client=mongo_client).save_resume(resume_name=data.get("resume_name"), data=data)
print(base64_string)
