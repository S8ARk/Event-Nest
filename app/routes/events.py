from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models.event import Category, Event
from app.forms.event import EventForm
from app.utils.decorators import organizer_required, requires_onboarding
from app.services.event_service import create_event, update_event, delete_event, get_catalog_events, EventPermissionError

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('/')
@requires_onboarding
def catalog():
    """
    Renders the primary event discovery catalog.
    
    Handles category filtering and title/description search queries, returning a sorted feed of active events.
    """
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('q', type=str)
    
    events = get_catalog_events(category_id, search_query)
    categories = Category.query.all()
    
    return render_template('events/catalog.html', events=events, categories=categories, current_category=category_id, search_query=search_query)

@bp.route('/<int:event_id>')
@requires_onboarding
def detail(event_id):
    """
    Retrieves and displays the full details of a specific active event mapping.
    """
    event = Event.query.get_or_404(event_id)
    if not event.is_active:
        abort(404)
    return render_template('events/detail.html', event=event)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
@organizer_required
def create():
    """
    Renders the event creation form and processes new event submissions to the service layer.
    """
    form = EventForm()
    # Populate choices from DB
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        event = create_event(form.data, current_user.id)
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
        
    return render_template('events/form.html', form=form, title='Create New Event')

@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit(event_id):
    """
    Authorizes the organizer and processes modifications to their existing event mapping.
    """
    event = Event.query.get_or_404(event_id)
    
    # Pre-authorize before form load
    if event.organizer_id != current_user.id and current_user.role != 'admin':
        abort(403)
        
    form = EventForm(obj=event)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        try:
            update_event(event.id, form.data, current_user.id, current_user.role)
            flash('Event updated successfully!', 'success')
            return redirect(url_for('events.detail', event_id=event.id))
        except EventPermissionError:
            abort(403)
            
    return render_template('events/form.html', form=form, title='Edit Event', event=event)

@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
@organizer_required
def delete(event_id):
    """
    Triggers a soft-delete archiving process for an event if the operator has authorization.
    """
    try:
        delete_event(event_id, current_user.id, current_user.role)
        flash('Event has been archived.', 'info')
    except EventPermissionError:
        abort(403)
    return redirect(url_for('user.dashboard'))
