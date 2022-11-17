# OpenclassroomsProject-P10
OpenClassRooms Project-P10 est un projet Python ayant un but d'apprentissage dans le cadre de la formation OpenClassRooms Développeur d'Application Python.  
Thème du projet : Créez une API sécurisée RESTful en utilisant Django REST.

## Installation

### 1. Récupération du projet sur votre machine locale

Clonez le repository sur votre machine.

```bash
git clone https://github.com/GDSDC/OpenclassroomsProject-P10.git
```

Accédez au répertoire cloné.
```bash
cd OpenclassroomsProject-P10
```

### 2. Création d'un environnement virtuel 
Créez l'environnement virtuel env.
```python
python3 -m venv env
```

### 3. Activation et installation de votre environnement virtuel 

Activez votre environnement virtuel env nouvellement créé.
```bash
source env/bin/activate
```

Installez les paquets présents dans la liste requirements.txt.
```bash
pip install -r requirements.txt
```

### 4. Initialisation de la base de données

Accédez au dossier de travail.
```bash
cd softdesk
```

Procédez à une recherche de migrations.
```bash
python manage.py makemigrations
```

Lancer les migrations nécessaires.
```bash
python manage.py migrate
```

## Utilisation

### 1. Démarrage du serveur local

Accédez au dossier de travail.
```bash
cd softdesk
```

Démarrez le serveur local.
```python
python manage.py runserver
```