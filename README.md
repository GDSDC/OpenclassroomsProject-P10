<h3 align="center">
    <img alt="Logo" title="#logo" width="236px" src="/assets/16007803099977_P8.png">
    <br>
</h3>


# OpenClassrooms Projet P10

- [Objectif](#obj)
- [Compétences](#competences)
- [Technologies](#techs)
- [Requirements](#reqs)
- [Architecture](#architecture)
- [Configuration locale](#localconfig)
- [Documentation](#docs)
- [Présentation](#presentation)

<a id="obj"></a>
## Objectif

SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B. 
L'objectif du projet est de créer un back-end performant et sécurisé (API sécurisée RESTful en utilisant Django REST), devant servir les applications sur toutes les plateformes. 
<a id="competences"></a>
## Compétences acquises
- Documenter une application
- Créer une API RESTful avec Django REST
- Sécuriser une API afin qu'elle respecte les normes OWASP et RGPD

<a id="techs"></a>
## Technologies Utilisées
- [Python3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [DjangoRestFramework](https://www.django-rest-framework.org/)
- [JWT](https://jwt.io/)
- [Sqlite](https://www.sqlite.org/)

<a id="reqs"></a>
## Requirements
- django
- djangorestframework
- djangorestframework-simplejwt
- python-dotenv

<a id="architecture"></a>
## Architecture et répertoires
```
Project
├── softdesk
│   ├── api
│   ├── core : répertoire contenant notre application principale
│   │    ├── comments
│   │    ├── contributors
│   │    ├── issues
│   │    ├── projects
│   │    ├── users
│   ├── softdesk : répertoire du projet django
│   │    ├── settings.py : fichier de réglages django
│   │    ├── urls.py : fichier principal des endpoints
│   │    ├── ..
│   ├── db.sqlite3 : base de données
│   ├── manage.py : fichier principal de gestion django
│
|── requirements.txt
|── documentation
|── postman
```

<a id="localconfig"></a>
## Configuration locale
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
```bash
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

<a id="docs"></a>
## Documentation

Retrouvez la documentation de l'api sur postman : https://documenter.getpostman.com/view/11247386/VUqyoZZ5

<a id="presentation"></a>
### Présentation

[<img alt="presentation" width="480px" src="/assets/presentation.png">](https://docs.google.com/presentation/d/e/2PACX-1vSaQDFZqITRuUdy0DRTfTtYnIbvV5aEz0TO_yQu6_NSeEX5aM79u0oMW9o6W5RGrojn3meSMsRnsFRt/pub?start=true&loop=false&delayms=5000)