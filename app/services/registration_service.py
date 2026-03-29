from app import db
from app.models.event import Event
from app.models.interaction import Registration, InteractionLog

class RegistrationError(Exception):
    """Custom exception for registration logic failures."""
    pass

def register_user_for_event(user_id: int, event_id: int) -> str:
    """Handles the business logic of registering a user for an event, validating capacity, and mapping interaction flows."""
    event = Event.query.get(event_id)
    if not event or not event.is_active:
        raise RegistrationError("This event is no longer active.")
        
    existing_reg = Registration.query.filter_by(user_id=user_id, event_id=event.id).first()
    
    if existing_reg:
        if existing_reg.status == 'cancelled':
            existing_reg.status = 'registered'
            log = InteractionLog(user_id=user_id, event_id=event.id, action_type='register')
            db.session.add(log)
            db.session.commit()
            return "Successfully re-registered for this event!"
        else:
            raise RegistrationError("You are already registered for this event.")
            
    active_regs = Registration.query.filter_by(event_id=event.id, status='registered').count()
    if event.max_capacity and active_regs >= event.max_capacity:
        raise RegistrationError("Sorry, this event has reached its maximum capacity.")
        
    registration = Registration(user_id=user_id, event_id=event.id)
    db.session.add(registration)
    
    log = InteractionLog(user_id=user_id, event_id=event.id, action_type='register')
    db.session.add(log)
    
    db.session.commit()
    return "Successfully registered for the event!"

def cancel_user_registration(user_id: int, event_id: int) -> str:
    """Handles the cancellation of a user's event registration and logs the withdrawal anomaly."""
    registration = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if not registration:
        raise RegistrationError("Registration not found.")
        
    if registration.status == 'registered':
        registration.status = 'cancelled'
        log = InteractionLog(user_id=user_id, event_id=event_id, action_type='cancel')
        db.session.add(log)
        db.session.commit()
        return "You have cancelled your registration for this event."
    return "Registration is already cancelled."
