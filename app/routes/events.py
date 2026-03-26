from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.event import Event, Category
from app.forms.event import EventForm
from app.utils.decorators import organizer_required, requires_onboarding

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('/')
@requires_onboarding
def catalog():
    # Filtering and standard catalog browsing (for all users including anon)
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('q', type=str)
    
    query = Event.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
        
    if search_query:
        query = query.filter(Event.title.ilike(f'%{search_query}%') | Event.description.ilike(f'%{search_query}%'))
        
    events = query.order_by(Event.date.asc(), Event.time.asc()).all()
    categories = Category.query.all()
    
    return render_template('events/catalog.html', events=events, categories=categories, current_category=category_id, search_query=search_query)

@bp.route('/<int:event_id>')
@requires_onboarding
def detail(event_id):
    event = Event.query.get_or_404(event_id)
    if not event.is_active:
        abort(404)
    return render_template('events/detail.html', event=event)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
@organizer_required
def create():
    form = EventForm()
    # Populate the category choices from the database
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            category_id=form.category_id.data,
            organizer_id=current_user.id,
            date=form.date.data,
            time=form.time.data,
            location=form.location.data,
            max_capacity=form.max_capacity.data
        )
        
        # In Module 5, we call NLP tokenization here to generate keywords
        from app.services.nlp_utils import extract_keywords
        event.keywords = extract_keywords(event.description) 
        
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
        
    return render_template('events/form.html', form=form, title='Create New Event')

@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Ensure only the organizer who created it (or admin) can edit
    if event.organizer_id != current_user.id and current_user.role != 'admin':
        abort(403)
        
    form = EventForm(obj=event)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.category_id = form.category_id.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.max_capacity = form.max_capacity.data
        
        # NLP keyword update
        from app.services.nlp_utils import extract_keywords
        event.keywords = extract_keywords(event.description)
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
        
    return render_template('events/form.html', form=form, title='Edit Event', event=event)

@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
@organizer_required
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.organizer_id != current_user.id and current_user.role != 'admin':
        abort(403)
        
    # Soft delete
    event.is_active = False
    db.session.commit()
    flash('Event has been archived.', 'info')
    return redirect(url_for('user.dashboard'))
