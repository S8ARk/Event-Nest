from app.models.user import User, Interest, UserInterest
from app.models.event import Event
from app.models.interaction import Recommendation
from app.services.nlp_utils import tokenize_interests
from flask import current_app
from collections import Counter
from app import db

def calculate_similarity(user_weighted_tokens: dict, event_keywords_list: list) -> float:
    """
    Calculates overlap score using weighted Frequency Distribution between 
    user preferences and event lemmas.
    """
    if not event_keywords_list or not user_weighted_tokens:
        return 0.0
        
    # Calculate Term Frequency (TF) of the event keywords
    event_freq = Counter(event_keywords_list)
    total_event_terms = len(event_keywords_list)
    
    if total_event_terms == 0:
        return 0.0
        
    semantic_score = 0.0
    
    # For every unique token in the event
    for token, count in event_freq.items():
        if token in user_weighted_tokens:
            # Term Frequency * User Priority Weight
            tf = count / total_event_terms
            weight = user_weighted_tokens[token]
            semantic_score += (tf * weight)
            
    # Normalize score to an understandable 0-100 percentage
    # (Multiply by an arbitrary scaling factor configured through testing)
    scaled_score = (semantic_score * 300.0) 
    
    # Cap at 100%
    return min(round(scaled_score, 2), 100.0)

def generate_recommendations_for_user(user_id: int):
    """
    Batch builds and caches personalized recommendations using advanced NLTK heuristics.
    """
    user = User.query.get(user_id)
    if not user or user.role != 'student':
        return []

    # 1. Build a weighted dictionary of User's Interest Tokens
    # Example: {'robotics': 1.5, 'computer': 1.0, 'science': 1.0}
    user_weighted_tokens = {}
    user_interest_names = []
    
    for ui in user.user_interests:
        interest = ui.interest
        if interest:
            user_interest_names.append(interest.name)
            # Tokenize & Lemmatize the single interest name
            lemmas = tokenize_interests([interest.name])
            for lemma in lemmas:
                # Store the token with the user's priority weight (default 1.0)
                # If lemma exists from multiple interests, take the max weight
                if lemma in user_weighted_tokens:
                    user_weighted_tokens[lemma] = max(user_weighted_tokens[lemma], ui.weight)
                else:
                    user_weighted_tokens[lemma] = ui.weight
    
    if not user_weighted_tokens:
        return []
        
    # 2. Get all active events the user hasn't registered for yet
    registered_event_ids = [reg.event_id for reg in user.registrations if reg.status == 'registered']
    active_events = Event.query.filter_by(is_active=True).all()
    
    # Clear old recommendations caching
    Recommendation.query.filter_by(user_id=user_id).delete()
    
    scored_events = []
    for event in active_events:
        if event.id in registered_event_ids:
            continue
            
        if not event.keywords:
            continue
            
        # Parse the comma-separated string back into a list of lemmas
        event_keywords_list = event.keywords.split(',')
        
        # Calculate Weighted Semantic Overlap
        score = calculate_similarity(user_weighted_tokens, event_keywords_list)
        
        # Add slight artificial boost if event category matches exact interest name
        if event.category and event.category.name in user_interest_names:
            score += 15.0
            score = min(score, 100.0)
            
        min_threshold = current_app.config.get('MIN_SCORE_THRESHOLD', 15.0)
        if score >= min_threshold:
            # Reconstruct the matched context
            matched_terms = [t for t in event_keywords_list if t in user_weighted_tokens]
            top_matches = list(set(matched_terms))[:3]
            
            reason = f"Matches your interest in topics related to {', '.join(top_matches)}." if top_matches else "Based on your selected interests."
            
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
    return scored_events[:10]

def get_cached_recommendations(user_id: int):
    """
    Fetches the latest pre-computed recommendations from the database cache.
    """
    recs = Recommendation.query.filter_by(user_id=user_id).order_by(Recommendation.score.desc()).limit(10).all()
    return recs
