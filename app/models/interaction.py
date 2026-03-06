from datetime import datetime, timezone
from app import db

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default='registered') # registered, cancelled, waitlisted

    def __repr__(self):
        return f'<Registration User:{self.user_id} Event:{self.event_id}>'

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    generated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Recommendation User:{self.user_id} Event:{self.event_id} Score:{self.score}>'

class InteractionLog(db.Model):
    __tablename__ = 'interaction_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    action_type = db.Column(db.String(50), nullable=False) # view, click, register
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    metadata_info = db.Column(db.Text, nullable=True) # device, duration, etc.

    def __repr__(self):
        return f'<Interaction User:{self.user_id} Action:{self.action_type}>'
