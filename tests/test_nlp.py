from app.services.nlp_utils import extract_keywords, tokenize_interests
from app.services.recommender import calculate_similarity

def test_extract_keywords():
    # Stop words and short words should be filtered
    text = "The quick brown fox jumps over the lazy dog."
    keywords = extract_keywords(text)
    
    # "the", "over" should be removed. "quick", "brown", "fox", "jumps", "lazy", "dog" should remain.
    # Note: depends on punkt being installed, but we have a fallback split() in the code.
    assert "quick" in keywords
    assert "brown" in keywords
    assert "jumps" in keywords
    
def test_tokenize_interests():
    interests = ["Artificial Intelligence", "Sports"]
    tokens = tokenize_interests(interests)
    
    assert "artificial" in tokens
    assert "intelligence" in tokens
    assert "sports" in tokens
    assert len(tokens) == 3
    
def test_calculate_similarity():
    # 50% match
    user_words = set(["math", "science", "coding"])
    event_words = ["coding", "science", "art", "music"]
    
    score = calculate_similarity(user_words, event_words)
    assert score == 50.0  # 2 matching / 4 total = 50%
    
    # 0% match
    score_zero = calculate_similarity(set(["sports"]), ["music", "art"])
    assert score_zero == 0.0
