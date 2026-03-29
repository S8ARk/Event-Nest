from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.registration_service import register_user_for_event, cancel_user_registration, RegistrationError
from app.utils.decorators import student_required

bp = Blueprint('registrations', __name__, url_prefix='/register')

@bp.route('/<int:event_id>', methods=['POST'])
@login_required
@student_required
def rsvp(event_id):
    try:
        success_message = register_user_for_event(current_user.id, event_id)
        flash(success_message, 'success')
    except RegistrationError as e:
        err_msg = str(e)
        flash(err_msg, 'danger' if 'capacity' in err_msg or 'active' in err_msg else 'info')
        
    return redirect(url_for('events.detail', event_id=event_id))

@bp.route('/<int:event_id>/cancel', methods=['POST'])
@login_required
@student_required
def cancel(event_id):
    try:
        message = cancel_user_registration(current_user.id, event_id)
        flash(message, 'info')
    except RegistrationError as e:
        flash(str(e), 'danger')
        
    return redirect(url_for('events.detail', event_id=event_id))
