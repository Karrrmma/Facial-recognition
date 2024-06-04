import base64
from flask import Flask, Response
import cv2
import face_recognition
import numpy as np
from pymongo import MongoClient
import os


client = MongoClient('mongodb://localhost:27017/')
db = client.recog
face = db.face


def load_and_store_faces(folder_path, name_mapping):
    for filename in os.listdir(folder_path):
        try:
            # Check if the file has the correct .jpg or .jpeg extension
            if filename.lower().endswith(('.jpg', '.jpeg')):
                # Check if the file is in the name mapping
                if filename not in name_mapping:
                    print(f"Warning: No name specified for {filename}. Skipping.")
                    continue
                # Get the name from the mapping
                name = name_mapping[filename]
                image_path = os.path.join(folder_path, filename)
                # Read and encode the image to base64
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
                # Check if the entry already exists in the database
                existing_entry = face.find_one({'name': name})
                if existing_entry is None:
                    # Insert into MongoDB
                    face.insert_one({'name': name, 'image_data': encoded_image})
                    print(f"Inserted {name} into the database.")
                else:
                    print(f"Entry for {name} already exists. Skipping.")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


# Call the function with the appropriate arguments
folder_path = 'folder'
name_mapping = {
    'Karma.jpg': 'Karma',
    'obama.jpg': 'Obama'
    # Add more mappings as needed
}
load_and_store_faces(folder_path, name_mapping)
