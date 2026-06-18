from flask import Blueprint, render_template, request, redirect
from app.models import db
from app.models.event import Event

view_bp = Blueprint('view', __name__)

# PAGE LOGIN
@view_bp.route("/")
def index():
    return render_template("index.html")


# EVENTS UTILISATEUR (DYNAMIQUE)
@view_bp.route("/events")
def events():
    events = Event.query.all()
    return render_template("events.html", events=events)


# ADMIN DASHBOARD (DYNAMIQUE)
@view_bp.route("/admin/events")
def admin_events():
    events = Event.query.all()
    return render_template("admin_dash.html", events=events)


# PAGE CREATE EVENT (FORM)
@view_bp.route("/admin/events/create", methods=["GET"])
def create_event():
    return render_template("create_event.html")


# CREATE EVENT (POST)
@view_bp.route("/admin/events/create", methods=["POST"])
def create_event_post():
    data = request.form

    new_event = Event(
        event_name=data.get("title"),
        event_date=data.get("date"),
        location=data.get("location"),
        description=data.get("description"),
        seats_available=100  # valeur par défaut
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect("/admin/events")


# DELETE EVENT
@view_bp.route("/admin/events/delete/<int:id>", methods=["POST"])
def delete_event(id):
    event = Event.query.get(id)

    if event:
        db.session.delete(event)
        db.session.commit()

    return redirect("/admin/events")


# DASHBOARD UTILISATEUR
@view_bp.route("/my-reservations")
def my_reservations():
    return render_template("user_dash.html")