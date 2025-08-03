import os
from fastapi import FastAPI, HTTPException
import logging

app = FastAPI()

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# Dossier de la base de données de reconnaissance faciale
DB_DIR = './db'

@app.delete("/delete_user")
async def delete_user(username: str):
    user_img_path = os.path.join(DB_DIR, f'{username}.jpg')
    user_pkl_path = os.path.join(DB_DIR, f'{username}_encoding.pkl')

    img_deleted = False
    pkl_deleted = False

    logging.info(f"Trying to delete image: {user_img_path}")
    if os.path.exists(user_img_path):
        os.remove(user_img_path)
        img_deleted = True
        logging.info(f"Image deleted: {user_img_path}")
    else:
        logging.warning(f"Image does not exist: {user_img_path}")

    logging.info(f"Trying to delete pkl file: {user_pkl_path}")
    if os.path.exists(user_pkl_path):
        try:
            os.remove(user_pkl_path)
            pkl_deleted = True
            logging.info(f"PKL file deleted: {user_pkl_path}")
        except PermissionError as e:
            logging.error(f"PermissionError: {e}")
        except OSError as e:
            logging.error(f"OSError: {e}")
    else:
        logging.warning(f"PKL file does not exist: {user_pkl_path}")

    if img_deleted and pkl_deleted:
        return {"message": f"The image and pkl file for user {username} have been successfully deleted!"}
    elif img_deleted:
        return {"message": f"The image for user {username} has been successfully deleted, but the pkl file does not exist!"}
    elif pkl_deleted:
        return {"message": f"The pkl file for user {username} has been successfully deleted, but the image does not exist!"}
    else:
        raise HTTPException(status_code=404, detail=f"Neither the image nor the pkl file for user {username} exist!")