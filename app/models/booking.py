from datetime import datetime
from app.models import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), nullable=False, default='pending')

    number_tickets = db.Column(db.Integer, default=1)

    #  RELATIONS PROPREMENT NOMMÉES
    user = db.relationship("User", backref="user_bookings")
    event = db.relationship("Event", back_populates="bookings")
