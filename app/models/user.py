from datetime import datetime, timezone
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') # student, organizer, admin
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    has_completed_onboarding = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    user_interests = db.relationship('UserInterest', backref='user', lazy=True, cascade="all, delete-orphan")
    registrations = db.relationship('Registration', backref='user', lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade="all, delete-orphan")
    interactions = db.relationship('InteractionLog', backref='user', lazy=True, cascade="all, delete-orphan")
    
    # Organizer relationships
    organized_events = db.relationship('Event', backref='organizer', lazy=True)

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'

class Interest(db.Model):
    __tablename__ = 'interests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # keywords represents the NLTK tokenized topics
    keywords = db.Column(db.Text, nullable=True) 
    
    users = db.relationship('UserInterest', backref='interest', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Interest {self.name}>'

class UserInterest(db.Model):
    __tablename__ = 'user_interests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False, default=1.0) # Priority weighting
