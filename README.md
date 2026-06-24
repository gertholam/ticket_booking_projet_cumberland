
## EventFlow - Application de Réservation de Billets
EventFlow est une application web développée avec Flask permettant la gestion d’événements, la réservation de billets par les utilisateurs et l’administration complète via un tableau de bord.

## Fonctionnalités
### Utilisateur

Création de compte et authentification sécurisée
Consultation des événements disponibles
Réservation de billets
Consultation et gestion des réservations (annulation possible)

### Administrateur

#### Gestion des événements :

Création
Modification
Suppression


#### Gestion des réservations :

Visualisation de toutes les réservations
Acceptation ou refus des demandes


#### Accès au tableau de bord administrateur


#### Sécurité
##### L’application intègre plusieurs mécanismes de sécurité :

Hash des mots de passe avec Flask-Bcrypt
Gestion des rôles (administrateur / utilisateur)
Protection des routes sensibles
Validation des entrées utilisateur
Protection CSRF
Limitation des requêtes (rate limiting)
Headers de sécurité


#### Technologies utilisées

Python 3
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-Bcrypt
Flask-JWT-Extended
Flask-Limiter
Flask-Talisman
MySQL


#### Structure du projet
ticket_booking/
│
├── run.py                 # Point d’entrée de l’application
│
├── app/
│   ├── __init__.py        # Initialisation de l’application
│   ├── config.py          # Configuration
│   ├── models/            # Modèles de données (User, Event, Booking)
│   ├── routes/            # Routes Flask (auth, view)
│   ├── templates/         # Templates HTML (Jinja2)
│   ├── static/            # Fichiers statiques (CSS, images)
│   ├── security.py        # Gestion de la sécurité
│
└── instance/              # Configuration locale / base de données


## Installation
1. Cloner le dépôt
Shellgit clone https://github.com/gertholam/ticket_booking_projet_cumberland.gitcd ticket_booking_projet_cumberlandShow more lines

2. Créer un environnement virtuel
Shellpython -m venv .venvShow more lines
Activation :

## PowerShell :

Shell.venv\Scripts\Activate.ps1Show more lines

CMD :

Shell.venv\Scripts\activate.batShow more lines

3. Installer les dépendances
Shellpip install -r requirements.txtShow more lines

4. Configurer la base de données
Modifier le fichier :
app/config.py

Exemple :
PythonSQLALCHEMY_DATABASE_URI = "mysql+pymysql://userShow more lines

## Lancer l’application
Shellcd ticket_bookingpython run.pyShow more lines
L’application sera accessible à l’adresse :
http://127.0.0.1:5000


### Utilisation
Accès utilisateur

Page d’accueil : /
Consultation des événements : /events
Réservations : /my-reservations

### Accès administrateur

Gestion des événements : /admin/events
Gestion des réservations : /admin/bookings


### Améliorations possibles

Pagination des événements
Recherche et filtres
Notifications par email
Déploiement (Docker ou cloud)
Gestion avancée des rôles


### Contexte
Projet réalisé dans le cadre du cours
Développement de logiciels et sécurité des applications
au Collège Cumberland.

Auteur
Gertho Islmak Lamusique

----------------------------------------------------


# EventFlow Ticket Booking App

EventFlow is a Flask-based ticket booking web application for event management, user reservations, and admin operations.

## Features

- User authentication and profile management
- Event browsing, reservation creation, and reservation history
- Admin dashboard for events, bookings, and user management
- CSRF token support and rate limiting via Flask-Limiter
- Security headers with Flask-Talisman

## Tech Stack

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-Limiter
- Flask-Talisman
- MySQL database backend

## Repository Structure

- `ticket_booking/`
  - `run.py` — app entrypoint
  - `app/` — application package
    - `__init__.py` — app factory and extension initialization
    - `config.py` — app configuration values
    - `models/` — SQLAlchemy models for users, events, and bookings
    - `routes/` — Flask blueprints and request handlers
    - `templates/` — Jinja2 HTML templates
    - `static/` — static assets such as CSS
    - `security.py` — CSRF and auth helper utilities

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# or
.venv\Scripts\activate.bat   # Windows CMD
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Update database configuration in `ticket_booking/app/config.py`.
   - Default uses MySQL with SQLAlchemy.
   - Change `SQLALCHEMY_DATABASE_URI` to match your environment.

## Running the App

From the repository root:

```bash
cd ticket_booking
.venv\Scripts\python.exe run.py
```

The application will start in debug mode on `http://127.0.0.1:5000`.

## Usage

- Open `/` to access the login page.
- Use the navigation sidebar to browse events and view reservations.
- Admins can access admin pages such as `/admin/events`, `/admin/bookings`, and `/admin/users`.
