from app.models.user import User, Interest
from app.models.event import Event
from app.models.interaction import Recommendation
from app.services.nlp_utils import tokenize_interests
from app import db

MIN_SCORE_THRESHOLD = 15.0  # Percentage

def calculate_similarity(user_keywords: set, event_keywords: list) -> float:
    """
    Calculates overlap percentage between what a user likes and an event's tokens.
    """
    if not event_keywords or not user_keywords:
        return 0.0
        
    event_keywords_set = set(event_keywords)
    
    # Find intersection of words
    matching_keywords = user_keywords.intersection(event_keywords_set)
    
    # Score = (Matches / Total Event Keywords) * 100
    if len(event_keywords_set) == 0:
        return 0.0
        
    score = (len(matching_keywords) / len(event_keywords_set)) * 100.0
    return round(score, 2)

def generate_recommendations_for_user(user_id: int):
    """
    Batch builds and caches personalized recommendations using NLTK keywords.
    """
    user = User.query.get(user_id)
    if not user or user.role != 'student':
        return []

    # 1. Get raw interest names the user selected
    user_interest_names = [ui.interest.name for ui in user.user_interests if ui.interest]
    
    # 2. Extract NLTK tokens from those names
    user_keywords = set(tokenize_interests(user_interest_names))
    
    if not user_keywords:
        return [] # Cold start problem: User has no interests set
        
    # 3. Get all active events the user hasn't registered for yet
    registered_event_ids = [reg.event_id for reg in user.registrations if reg.status == 'registered']
    active_events = Event.query.filter_by(is_active=True).all()
    
    # Clear old recommendations for this user
    Recommendation.query.filter_by(user_id=user_id).delete()
    
    scored_events = []
    for event in active_events:
        if event.id in registered_event_ids:
            continue # Don't recommend events they are already attending
            
        if not event.keywords:
            continue
            
        # Parse the comma-separated string back into a list
        event_keywords_list = event.keywords.split(',')
        
        # Calculate overlap
        score = calculate_similarity(user_keywords, event_keywords_list)
        
        # Add slight boost if event category matches exact interest name
        if event.category.name in user_interest_names:
            score += 10.0
            
        if score >= MIN_SCORE_THRESHOLD:
            # Create DB Cache entity
            reason = f"Matches your interest in topics related to {', '.join(list(user_keywords)[:3])}."
            rec = Recommendation(user_id=user_id, event_id=event.id, score=score, reason=reason)
            db.session.add(rec)
            
            scored_events.append({
                'event': event,
                'score': score,
                'reason': reason
            })
            
    db.session.commit()
    
    # Sort by descending score
    scored_events.sort(key=lambda x: x['score'], reverse=True)
    return scored_events[:10] # Return top 10

def get_cached_recommendations(user_id: int):
    """
    Fetches the latest pre-computed recommendations from the database cache.
    """
    recs = Recommendation.query.filter_by(user_id=user_id).order_by(Recommendation.score.desc()).limit(10).all()
    return recs
