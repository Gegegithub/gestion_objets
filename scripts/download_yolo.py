#!/usr/bin/env python
"""
Script pour télécharger le modèle YOLOv8 nécessaire au projet.
"""

import os
import sys
import requests
from pathlib import Path

# Ajouter le dossier parent au chemin Python pour pouvoir importer les paramètres Django
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestionob.settings')

from dotenv import load_dotenv
load_dotenv()

def download_yolo_model():
    # URL du modèle YOLOv8n
    model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
    
    # Récupérer le chemin du modèle depuis les variables d'environnement ou utiliser la valeur par défaut
    model_path = os.getenv('YOLO_MODEL_PATH', 'yolov8n.pt')
    
    if os.path.exists(model_path):
        print(f"Le modèle {model_path} existe déjà. Téléchargement ignoré.")
        return
    
    print(f"Téléchargement du modèle YOLOv8 depuis {model_url}...")
    
    try:
        # Télécharger le modèle
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        # Écrire le fichier
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Modèle téléchargé avec succès et enregistré à {model_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement du modèle: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_yolo_model() 