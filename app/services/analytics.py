from app import db
from app.models.user import User
from app.models.event import Event
from app.models.interaction import Registration, InteractionLog, Recommendation
from sqlalchemy import func

def get_system_metrics() -> dict:
    """
    Calculates essential system-wide KPIs for the Admin Dashboard.
    """
    metrics = {}
    
    # 1. User Metrics
    metrics['total_users'] = User.query.count()
    metrics['total_students'] = User.query.filter_by(role='student').count()
    metrics['total_organizers'] = User.query.filter_by(role='organizer').count()
    
    # 2. Event Metrics
    metrics['total_events'] = Event.query.count()
    metrics['active_events'] = Event.query.filter_by(is_active=True).count()
    
    # 3. Engagement Metrics
    metrics['total_registrations'] = Registration.query.filter_by(status='registered').count()
    
    # 4. Recommendation Engine Efficacy
    # How many interactions were driven by the recommender (placeholder concept)
    metrics['total_recommendations_generated'] = Recommendation.query.count()
    
    return metrics

def get_popular_events(limit: int = 5) -> list:
    """
    Returns the top N events based on number of active registrations.
    """
    popular_events = db.session.query(
        Event, 
        func.count(Registration.id).label('reg_count')
    ).join(Registration).filter(
        Registration.status == 'registered'
    ).group_by(Event.id).order_by(
        db.text('reg_count DESC')
    ).limit(limit).all()
    
    return popular_events
