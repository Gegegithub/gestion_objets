# Gestion d'Objets avec IA

Une application Django permettant de cataloguer des objets (défectueux ou non) avec une fonctionnalité d'analyse d'images par intelligence artificielle (YOLOv8).

## Fonctionnalités

- 📋 **Gestion d'inventaire**
  - Catalogage d'objets avec leur état (défectueux/OK)
  - Description détaillée et ajout d'images
  - Système de corbeille et de restauration

- 🧠 **Analyse d'images par IA**
  - Détection d'objets avec YOLOv8
  - Visualisation des objets détectés avec leurs scores de confiance
  - Historique des analyses

- 🔐 **Authentification et sécurité**
  - Système d'inscription et connexion d'utilisateurs
  - Gestion des permissions (administrateurs/utilisateurs)
  - Protection des routes

- 📊 **Suivi des activités**
  - Journal détaillé des modifications
  - Traçabilité complète des actions

## Installation

1. Cloner le dépôt
   ```
   git clone https://github.com/votre-username/gestion-objets-ia.git
   cd gestion-objets-ia
   ```

2. Créer un environnement virtuel
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Installer les dépendances
   ```
   pip install -r requirements.txt
   ```

4. Configurer les variables d'environnement
   ```
   cp .env.example .env
   # Éditez le fichier .env selon vos besoins
   ```

5. Télécharger le modèle YOLOv8
   ```
   python scripts/download_yolo.py
   ```

6. Exécuter les migrations
   ```
   python manage.py migrate
   ```

7. Créer un superutilisateur
   ```
   python manage.py createsuperuser
   ```

8. Lancer le serveur
   ```
   python manage.py runserver
   ```

## Technologies utilisées

- 🐍 Django 5.1.x
- 🤖 YOLOv8 (via ultralytics)
- 🎨 Bootstrap 5
- 💾 SQLite (ou PostgreSQL en production)

## Structure du projet

```
.
├── authentication/      # Application d'authentification
├── gestionob/           # Configuration du projet
├── monappli/            # Application principale
├── scripts/             # Scripts utilitaires
├── static/              # Fichiers statiques
├── media/               # Fichiers média
├── manage.py            # Script de gestion Django
└── requirements.txt     # Dépendances Python
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations. 