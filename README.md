# Gestion Ecole API

Ce projet est une API développée avec FastAPI permettant de gérer une école.

Elle permet de :
- créer et supprimer des classes
- créer des étudiants
- ajouter ou retirer un étudiant d'une classe
- ajouter des notes à un étudiant
- calculer la moyenne d’un étudiant
- calculer la moyenne d’une classe

---

## Installation du projet

1. Cloner le repository :

git clone https://github.com/ilian7517/gestion-cole-fast-API.git

2. Aller dans le dossier :

cd gestion-cole-fast-API

3. Créer un environnement virtuel :

python -m venv venv

4. Activer l’environnement :

Windows :
source venv/Scripts/activate

5. Installer les dépendances :

pip install -r requirements.txt

---

## Lancer l’API

python -m uvicorn app.main:app --reload

Une fois lancé, l’API est accessible sur :

http://127.0.0.1:8000

La documentation Swagger est disponible sur :

http://127.0.0.1:8000/docs

---

## Routes principales

### Classes
- POST /classes
- GET /classes
- GET /classes/{class_id}
- DELETE /classes/{class_id}
- GET /classes/{class_id}/students

### Étudiants
- POST /students
- GET /students/{student_id}

### Gestion des étudiants dans une classe
- POST /classes/{class_id}/students/{student_id}
- DELETE /classes/{class_id}/students/{student_id}

### Notes
- POST /students/{student_id}/grades
- GET /students/{student_id}/average
- GET /classes/{class_id}/average

---

Projet réalisé dans le cadre du projet Python (projet 1 FastAPI).
