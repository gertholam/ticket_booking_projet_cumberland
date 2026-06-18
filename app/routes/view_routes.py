from flask import Blueprint, render_template, request, redirect
from app.models import db
from app.models.event import Event
from app.models.booking import Booking

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


# DASHBOARD UTILISATEUR + AFFICHAGE DES RÉSERVATIONS
@view_bp.route("/my-reservations")
def my_reservations():
    user_id = 1  # temporaire, remplacer par l'ID réel de l'utilisateur connecté
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return render_template("user_dash.html", bookings=bookings)


# CREATION DE RÉSERVATION
@view_bp.route("/reservations/create", methods=["POST"])
def create_booking():
    data = request.form
    user_id = 1  # Simuler un utilisateur connecté
    event_id = request.form.get("event_id", type=int)

    if event_id is None:
        return redirect("/events")

    new_booking = Booking(
        user_id=user_id,
        event_id=event_id,
        status='pending'
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect("/my-reservations")


# ANNULATION DE RÉSERVATION
@view_bp.route("/reservations/cancel/<int:id>", methods=["POST"])
def cancel_booking(id):
    booking = Booking.query.get(id)

    if booking:
        booking.status = "cancelled"
        db.session.commit()

    return redirect("/my-reservations")
