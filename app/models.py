from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_code = db.Column(db.String(6))
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_email_code(self):
        import random
        self.email_verification_code = str(random.randint(100000, 999999))
        return self.email_verification_code
    
    def __repr__(self):
        return f'<User {self.email}>'
    
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    from_location = db.Column(db.String(255), nullable=False)
    to_location = db.Column(db.String(255), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.Time)
    available_seats = db.Column(db.Integer, default=4)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    driver = db.relationship('User', backref=db.backref('trips', lazy=True))
    
    def __repr__(self):
        return f'<Trip {self.from_location} -> {self.to_location}>'
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seats = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    trip = db.relationship('Trip', backref=db.backref('bookings', lazy=True))
    passenger = db.relationship('User', backref=db.backref('bookings', lazy=True))
    
    def __repr__(self):
        return f'<Booking {self.id} - Trip {self.trip_id}>'