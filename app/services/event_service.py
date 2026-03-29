from app import db
from app.models.event import Event
from app.services.nlp_utils import extract_keywords

class EventPermissionError(Exception):
    """Exception raised when a user does not have permission to modify an event."""
    pass

def create_event(data: dict, organizer_id: int) -> Event:
    """Creates a new event and triggers the NLP keyword generation module in the background."""
    event = Event(
        title=data.get('title'),
        description=data.get('description'),
        category_id=data.get('category_id'),
        organizer_id=organizer_id,
        date=data.get('date'),
        time=data.get('time'),
        location=data.get('location'),
        max_capacity=data.get('max_capacity')
    )
    event.keywords = extract_keywords(event.description)
    db.session.add(event)
    db.session.commit()
    return event

def update_event(event_id: int, data: dict, user_id: int, user_role: str) -> Event:
    """Updates an existing event with stringent permissions and triggers NLP semantic recalculations."""
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != user_id and user_role != 'admin':
        raise EventPermissionError("You do not have permission to edit this event.")
        
    event.title = data.get('title')
    event.description = data.get('description')
    event.category_id = data.get('category_id')
    event.date = data.get('date')
    event.time = data.get('time')
    event.location = data.get('location')
    event.max_capacity = data.get('max_capacity')
    
    event.keywords = extract_keywords(event.description)
    db.session.commit()
    return event

def delete_event(event_id: int, user_id: int, user_role: str) -> Event:
    """Performs a soft delete of an event, archiving it without breaking cascading foreign keys."""
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != user_id and user_role != 'admin':
        raise EventPermissionError("You do not have permission to delete this event.")
        
    event.is_active = False
    db.session.commit()
    return event
    
def get_catalog_events(category_id=None, search_query=None):
    """Retrieves and seamlessly filters the global active event feed."""
    query = Event.query.filter_by(is_active=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search_query:
        query = query.filter(Event.title.ilike(f'%{search_query}%') | Event.description.ilike(f'%{search_query}%'))
        
    return query.order_by(Event.date.asc(), Event.time.asc()).all()
