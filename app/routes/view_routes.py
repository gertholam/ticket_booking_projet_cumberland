from flask import Blueprint, render_template, request, redirect, session
from app.models import db
from app.models.event import Event
from app.models.booking import Booking
from app.routes.auth_routes import is_admin

view_bp = Blueprint('view', __name__)

#  PAGE LOGIN
@view_bp.route("/")
def index():
    return render_template("index.html")


#  EVENTS UTILISATEUR (DYNAMIQUE)
@view_bp.route("/events")
def events():
    events = Event.query.all()
    return render_template("events.html", events=events)


#  CREATE EVENT 
@view_bp.route("/admin/events/create", methods=["GET", "POST"])
def create_event():

    if not is_admin():
        return redirect("/")

    if request.method == "GET":
        return render_template("create_event.html")

    #  POST
    data = request.form
    print(data)  # DEBUG

    new_event = Event(
        event_name=data.get("title"),
        event_date=data.get("date"),
        location=data.get("location"),
        description=data.get("description"),
        seats_available=100,
        categorie=data.get("categorie") or "General"
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect("/admin/events")


#  DELETE EVENT (FIX <int:id>)
@view_bp.route("/admin/events/delete/<int:id>", methods=["POST"])
def delete_event(id):

    if not is_admin():
        return redirect("/")

    event = Event.query.get(id)

    if event:
        db.session.delete(event)
        db.session.commit()

    return redirect("/admin/events")


#  DASHBOARD UTILISATEUR
@view_bp.route("/my-reservations")
def my_reservations():

    user_id = session.get("user_id")  
    if not user_id:
        return redirect("/")

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return render_template("user_dash.html", bookings=bookings)


#  CRÉER RÉSERVATION
@view_bp.route("/reservations/create", methods=["POST"])
def create_booking():

    user_id = session.get("user_id")  
    if not user_id:
        return redirect("/")

    event_id = request.form.get("event_id", type=int)

    if event_id is None:
        return redirect("/events")

    new_booking = Booking(
        user_id=user_id,
        event_id=event_id,
        status="pending",
        number_tickets=1   
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect("/my-reservations")


#  ANNULER RÉSERVATION (FIX <int:id>)
@view_bp.route("/reservations/cancel/<int:id>", methods=["POST"])
def cancel_booking(id):

    booking = Booking.query.get(id)

    if booking:
        booking.status = "cancelled"
        db.session.commit()

    return redirect("/my-reservations")


#  ADMIN DASHBOARD
@view_bp.route("/admin/events")
def admin_events():

    if not is_admin():
        return redirect("/")

    events = Event.query.all()
    return render_template("admin_dash.html", events=events)


#  ADMIN BOOKINGS
@view_bp.route("/admin/bookings")
def admin_bookings():

    if not is_admin():
        return redirect("/")

    bookings = Booking.query.all()

    return render_template("admin_bookings.html", bookings=bookings)


#  ACCEPT BOOKING
@view_bp.route("/admin/bookings/accept/<int:id>", methods=["POST"])
def accept_booking(id):

    if not is_admin():
        return redirect("/")

    booking = Booking.query.get(id)

    if booking:
        booking.status = "confirmed"
        db.session.commit()

    return redirect("/admin/bookings")


#  Refuser BOOKING
@view_bp.route("/admin/bookings/reject/<int:id>", methods=["POST"])
def reject_booking(id):

    if not is_admin():
        return redirect("/")

    booking = Booking.query.get(id)

    if booking:
        booking.status = "cancelled"
        db.session.commit()

    return redirect("/admin/bookings")


#  DÉTAIL EVENT
@view_bp.route("/admin/events/<int:id>")
def event_detail(id):

    if not is_admin():
        return redirect("/")

    event = Event.query.get(id)
    return render_template("event_detail.html", event=event)


#  LOGOUT
@view_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#  MOdifier EVENT 
@view_bp.route("/admin/events/edit/<int:id>", methods=["GET", "POST"])
def edit_event(id):

    if not is_admin():
        return redirect("/")

    event = Event.query.get(id)

    if not event:
        return redirect("/admin/events")

    if request.method == "GET":
        return render_template("edit_event.html", event=event)

    #  POST → update
    data = request.form

    event.event_name = data.get("title")
    event.event_date = data.get("date")
    event.location = data.get("location")
    event.description = data.get("description")
    event.categorie = data.get("categorie")

    db.session.commit()

    return redirect("/admin/events")
