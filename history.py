from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/access_history")
async def get_access_history():
    access_history_dir = "./access_history"
    access_history_files = []

    # Vérifie si le dossier existe
    if os.path.exists(access_history_dir) and os.path.isdir(access_history_dir):
        # Parcourt tous les fichiers du dossier
        for filename in os.listdir(access_history_dir):
            file_path = os.path.join(access_history_dir, filename)
            # Vérifie si c'est un fichier
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    # Lit le contenu du fichier et l'ajoute à la liste
                    content = file.read()
                    access_history_files.append({filename: content})

    return access_history_files

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.1.14", port=8000)