from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import shutil
import os
import face_recognition
import pickle

app = FastAPI()

# Endpoint pour enregistrer un nouvel utilisateur
@app.post("/register")
async def register_user(username: str = Form(...), image: UploadFile = File(...)):
    # Chemin où l'image de l'utilisateur sera stockée
    image_path = f"./db/{username}.jpg"
    encoding_path = f"./db/{username}_encoding.pkl"

    # Sauvegarde temporaire de l'image téléchargée
    temp_image_path = f"./db/temp_{username}.jpg"
    with open(temp_image_path, "wb") as temp_img:
        shutil.copyfileobj(image.file, temp_img)
    
    # Charger et encoder l'image temporaire
    new_image = face_recognition.load_image_file(temp_image_path)
    new_image_encoding = face_recognition.face_encodings(new_image)
    if not new_image_encoding:
        os.remove(temp_image_path)
        raise HTTPException(status_code=400, detail="No face found in the uploaded image.")
    new_image_encoding = new_image_encoding[0]

    # Vérifiez les visages déjà enregistrés
    for filename in os.listdir('./db'):
        if filename.endswith('.jpg') and not filename.startswith('temp_'):
            existing_image = face_recognition.load_image_file(f'./db/{filename}')
            existing_image_encoding = face_recognition.face_encodings(existing_image)
            if existing_image_encoding:
                existing_image_encoding = existing_image_encoding[0]
                match = face_recognition.compare_faces([existing_image_encoding], new_image_encoding)
                if match[0]:
                    os.remove(temp_image_path)
                    raise HTTPException(status_code=400, detail="Face already registered ")
    
    # Déplacer l'image temporaire à l'emplacement final
    os.rename(temp_image_path, image_path)

    # Sauvegarder l'encodage du visage dans un fichier pkl
    with open(encoding_path, 'wb') as f:
        pickle.dump(new_image_encoding, f)

    # Logique d'enregistrement d'utilisateur ici
    return {"message": "User registered successfully"}