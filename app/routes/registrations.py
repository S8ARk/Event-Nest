from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.event import Event
from app.models.interaction import Registration, InteractionLog
from app.utils.decorators import student_required

bp = Blueprint('registrations', __name__, url_prefix='/register')

@bp.route('/<int:event_id>', methods=['POST'])
@login_required
@student_required
def rsvp(event_id):
    event = Event.query.get_or_404(event_id)
    
    if not event.is_active:
        flash('This event is no longer active.', 'danger')
        return redirect(url_for('events.detail', event_id=event.id))
        
    # Check if already registered
    existing_reg = Registration.query.filter_by(user_id=current_user.id, event_id=event.id).first()
    
    if existing_reg:
        if existing_reg.status == 'cancelled':
            # Re-registering
            existing_reg.status = 'registered'
            db.session.commit()
            
            # Log interaction
            log = InteractionLog(user_id=current_user.id, event_id=event.id, action_type='register')
            db.session.add(log)
            db.session.commit()
            
            flash('Successfully re-registered for this event!', 'success')
        else:
            flash('You are already registered for this event.', 'info')
        return redirect(url_for('events.detail', event_id=event.id))

    # Check capacity limit
    active_regs = Registration.query.filter_by(event_id=event.id, status='registered').count()
    if event.max_capacity and active_regs >= event.max_capacity:
        flash('Sorry, this event has reached its maximum capacity.', 'danger')
        return redirect(url_for('events.detail', event_id=event.id))
        
    # First time registration
    registration = Registration(user_id=current_user.id, event_id=event.id)
    db.session.add(registration)
    
    # Track the interaction for Analytics & ML feedback loop later
    log = InteractionLog(user_id=current_user.id, event_id=event.id, action_type='register')
    db.session.add(log)
    
    db.session.commit()
    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('events.detail', event_id=event.id))

@bp.route('/<int:event_id>/cancel', methods=['POST'])
@login_required
@student_required
def cancel(event_id):
    event = Event.query.get_or_404(event_id)
    registration = Registration.query.filter_by(user_id=current_user.id, event_id=event.id).first_or_404()
    
    if registration.status == 'registered':
        registration.status = 'cancelled'
        
        log = InteractionLog(user_id=current_user.id, event_id=event.id, action_type='cancel')
        db.session.add(log)
        
        db.session.commit()
        flash('You have cancelled your registration for this event.', 'info')
        
    return redirect(url_for('events.detail', event_id=event.id))
