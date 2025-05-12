from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import base64

class ObjectAnalyzer:
    def __init__(self):
        # Charger le modèle YOLOv8
        self.model = YOLO('yolov8n.pt')  # Utilise le modèle pré-entraîné YOLOv8n

    def analyze_image_url(self, image_url):
        try:
            # Télécharger l'image depuis l'URL
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            
            # Effectuer la détection
            results = self.model(img)
            
            # Traiter les résultats
            detections = []
            for r in results:
                for box in r.boxes:
                    detection = {
                        'class': r.names[int(box.cls[0])],
                        'confidence': float(box.conf[0]),
                        'bbox': box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    }
                    detections.append(detection)
            
            # Obtenir l'image annotée du premier résultat
            annotated_img = results[0].plot()  # Cette méthode retourne une image numpy avec les annotations
            
            # Convertir l'image numpy en base64 pour l'affichage
            pil_img = Image.fromarray(annotated_img)
            buffered = BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'detections': detections,
                'message': f"Détecté {len(detections)} objets",
                'image_base64': img_str
            }
            
        except Exception as e:
            return {
                'success': False,
                'detections': [],
                'message': f"Erreur lors de l'analyse: {str(e)}",
                'image_base64': None
            } 