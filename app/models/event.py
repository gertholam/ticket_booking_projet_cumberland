from app.models import db

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255))
    seats_available = db.Column(db.Integer)
    categorie = db.Column(db.String(255))
    description = db.Column(db.Text)

    # ❌ SUPPRIMÉ :
    # bookings = db.relationship('Booking', backref='event', lazy=True)