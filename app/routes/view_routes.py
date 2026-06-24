from flask import Blueprint, render_template, request, redirect, session
from app.models import db
from app.models.event import Event
from app.models.user import User
from app.models.booking import Booking
from app.routes.auth_routes import is_admin

view_bp = Blueprint('view', __name__)

# ACCUEIL
@view_bp.route("/")
def index():
    return render_template("index.html")


# ÉVÉNEMENTS UTILISATEUR
@view_bp.route("/events")
def events():
    events = Event.query.all()
    return render_template("events.html", events=events)


@view_bp.route('/events/<int:id>')
def event_detail(id):
    event = Event.query.get(id)
    if not event:
        return redirect('/events')
    return render_template('event_detail.html', event=event)


# CRÉER UN ÉVÉNEMENT
@view_bp.route("/admin/events/create", methods=["GET", "POST"])
def create_event():

    if not is_admin():
        return redirect("/")

    if request.method == "GET":
        return render_template("create_event.html")

    data = request.form

    new_event = Event(
        event_name=data.get("event_name"),
        event_date=data.get("event_date"),
        location=data.get("location"),
        seats_available=data.get("seats_available", type=int),
        categorie=data.get("category"),
        description=data.get("description")
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect("/admin/events")


# ÉVÉNEMENTS ADMIN
@view_bp.route("/admin/events")
def admin_events():

    if not is_admin():
        return redirect("/")

    events = Event.query.all()
    return render_template("admin_dash.html", events=events)


@view_bp.route("/admin/events/<int:id>")
def admin_event_detail(id):

    if not is_admin():
        return redirect("/")

    event = Event.query.get(id)
    if not event:
        return redirect("/admin/events")

    return render_template("admin_event_detail.html", event=event)


# SUPPRIMER UN ÉVÉNEMENT
@view_bp.route("/admin/events/delete/<int:id>", methods=["POST"])
def delete_event(id):

    if not is_admin():
        return redirect("/")

    event = Event.query.get(id)

    if event:
        Booking.query.filter_by(event_id=event.id).delete()
        db.session.delete(event)
        db.session.commit()

    return redirect("/admin/events")


# MODIFIER UN ÉVÉNEMENT
@view_bp.route("/admin/events/edit/<int:id>", methods=["GET", "POST"])
def edit_event(id):

    if not is_admin():
        return redirect("/")

    event = Event.query.get(id)

    if request.method == "GET":
        return render_template("edit_event.html", event=event)

    data = request.form

    event.event_name = data.get("event_name")
    event.event_date = data.get("event_date")
    event.location = data.get("location")
    event.seats_available = data.get("seats_available", type=int)
    event.categorie = data.get("category")
    event.description = data.get("description")

    db.session.commit()

    return redirect("/admin/events")


# RÉSERVATIONS UTILISATEUR
@view_bp.route("/my-reservations")
def my_reservations():

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return render_template("user_dash.html", bookings=bookings)


# CRÉER RÉSERVATION
@view_bp.route("/reservations/create", methods=["POST"])
def create_booking():

    user_id = session.get("user_id")
    event_id = request.form.get("event_id", type=int)

    if not user_id or not event_id:
        return redirect("/events")

    existing = Booking.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return "Déjà réservé"

    event = Event.query.get(event_id)
    if not event:
        return redirect("/events")

    if event.seats_available <= 0:
        return "Plus de places disponibles"

    event.seats_available -= 1

    new_booking = Booking(
        user_id=user_id,
        event_id=event_id,
        status="pending",
        number_tickets=1
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect("/my-reservations")


# ANNULER RÉSERVATION
@view_bp.route("/reservations/cancel/<int:id>", methods=["POST"])
def cancel_booking(id):

    booking = Booking.query.get(id)

    if booking:
        booking.status = "cancelled"
        db.session.commit()

    return redirect("/my-reservations")


# RÉSERVATIONS ADMIN
@view_bp.route("/admin/bookings")
def admin_bookings():

    if not is_admin():
        return redirect("/")

    bookings = Booking.query.all()

    return render_template("admin_bookings.html", bookings=bookings)


@view_bp.route("/admin/bookings/cancel/<int:id>", methods=["POST"])
def cancel_admin_booking(id):

    if not is_admin():
        return redirect("/")

    booking = Booking.query.get(id)
    if booking:
        event = Event.query.get(booking.event_id)
        if event:
            event.seats_available = (event.seats_available or 0) + booking.number_tickets
        db.session.delete(booking)
        db.session.commit()

    return redirect("/admin/bookings")


@view_bp.route("/admin/users")
def admin_users():
    if not is_admin():
        return redirect("/")

    users = User.query.all()
    return render_template("admin_users.html", users=users)


@view_bp.route("/admin/users/create", methods=["GET", "POST"])
def create_user():
    if not is_admin():
        return redirect("/")

    if request.method == "GET":
        return render_template("create_user.html")

    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "client")

    if not username or not email or not password:
        return render_template("create_user.html", error="Tous les champs sont requis.")

    if User.query.filter_by(email=email).first():
        return render_template("create_user.html", error="Adresse e-mail déjà utilisée.")

    from app import bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/admin/users")


@view_bp.route("/admin/users/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    if not is_admin():
        return redirect("/")

    user = User.query.get(id)
    if not user:
        return redirect("/admin/users")

    if request.method == "GET":
        return render_template("edit_user.html", user=user)

    data = request.form
    user.username = data.get("username")
    user.email = data.get("email")
    user.role = data.get("role", "client")
    password = data.get("password")
    if password:
        from app import bcrypt
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")
    db.session.commit()

    return redirect("/admin/users")


@view_bp.route("/admin/users/delete/<int:id>", methods=["POST"])
def delete_user(id):
    if not is_admin():
        return redirect("/")

    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin/users")


# ACCEPTER RÉSERVATION
@view_bp.route("/admin/bookings/accept/<int:id>", methods=["POST"])
def accept_booking(id):

    booking = Booking.query.get(id)

    if booking:
        booking.status = "confirmed"
        db.session.commit()

    return redirect("/admin/bookings")


# REFUSER RÉSERVATION
@view_bp.route("/admin/bookings/reject/<int:id>", methods=["POST"])
def reject_booking(id):

    booking = Booking.query.get(id)

    if booking:
        booking.status = "cancelled"
        db.session.commit()

    return redirect("/admin/bookings")


# DÉCONNEXION
@view_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# PROFIL UTILISATEUR - afficher et mettre à jour le nom d'utilisateur et le mot de passe
@view_bp.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")

    user = User.query.get(user_id)
    if not user:
        session.clear()
        return redirect("/")

    if request.method == "GET":
        return render_template("profile.html", user=user)

    data = request.form
    username = data.get("username")
    password = data.get("password")
    password_confirm = data.get("password_confirm")
    email = data.get("email")
    role = data.get("role")

    is_admin_user = session.get("role") == "admin"
    error = None

    if not username:
        error = "Le nom d'utilisateur est requis."

    if is_admin_user and not email:
        error = "L'adresse e-mail est requise."

    if password and password != password_confirm:
        error = "Les mots de passe ne correspondent pas."

    if not error:
        existing_username = User.query.filter(User.username == username, User.id != user.id).first()
        if existing_username:
            error = "Ce nom d'utilisateur est déjà utilisé."

    if not error and is_admin_user:
        existing_email = User.query.filter(User.email == email, User.id != user.id).first()
        if existing_email:
            error = "Cette adresse e-mail est déjà utilisée."

    if error:
        return render_template("profile.html", user=user, error=error)

    user.username = username
    if is_admin_user:
        user.email = email
        user.role = role or user.role

    if password:
        from app import bcrypt
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    db.session.commit()
    session["username"] = user.username
    if is_admin_user:
        session["role"] = user.role

    return redirect("/profile")