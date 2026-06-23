import functools
import re
import secrets
from datetime import datetime
from flask import current_app, session, request, abort, redirect


def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(32)
    return session["_csrf_token"]


def validate_csrf_token(token):
    return bool(token and token == session.get("_csrf_token"))


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            current_app.logger.warning("Unauthorized access attempt to %s", request.path)
            return redirect("/")
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            current_app.logger.warning("Unauthorized admin access attempt to %s by user_id=%s", request.path, session.get("user_id"))
            return redirect("/")
        return view(*args, **kwargs)
    return wrapped


def validate_username(username):
    return bool(username) and 3 <= len(username) <= 50


def validate_password(password):
    return bool(password) and 8 <= len(password) <= 128


def validate_email(email):
    return bool(email) and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)


def validate_role(role):
    return role in ("admin", "client")


def validate_event_data(data):
    errors = []
    event_name = data.get("event_name", "").strip()
    event_date = data.get("event_date", "").strip()
    location = data.get("location", "").strip()
    seats = data.get("seats_available", "").strip()

    if not event_name:
        errors.append("Le nom de l'événement est requis.")
    if not event_date:
        errors.append("La date de l'événement est requise.")
    else:
        try:
            datetime.strptime(event_date, "%Y-%m-%d")
        except ValueError:
            errors.append("La date doit être au format AAAA-MM-JJ.")

    if not location:
        errors.append("Le lieu est requis.")

    if not seats:
        errors.append("Le nombre de places est requis.")
    else:
        try:
            seats_int = int(seats)
            if seats_int < 0:
                errors.append("Le nombre de places doit être positif ou nul.")
        except ValueError:
            errors.append("Le nombre de places est invalide.")

    return errors
