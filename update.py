import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Directory for facial recognition database
DB_DIR = './db'

# Ensure the directory exists
if not os.path.exists(DB_DIR):
    os.mkdir(DB_DIR)

@app.post("/update_photo")
async def update_photo(username: str = Form(...), new_photo: UploadFile = File(...)):
    user_img_path = os.path.join(DB_DIR, f'{username}.jpg')

    # Check if the user exists in the database
    if not os.path.exists(user_img_path):
        raise HTTPException(status_code=404, detail=f"User {username} not found!")

    # Save the new photo
    with open(user_img_path, "wb") as img_file:
        img_file.write(await new_photo.read())

    logging.info(f"New photo saved for user {username}")

    return {"message": f"New photo saved successfully for user {username}"}
