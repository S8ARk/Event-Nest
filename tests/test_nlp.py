from app.services.nlp_utils import extract_keywords, tokenize_interests
from app.services.recommender import calculate_similarity

def test_extract_keywords():
    text = "The quick brown fox jumps over the lazy dog. The fox is fast."
    keywords = extract_keywords(text)
    
    # Nouns and Adjectives should be extracted and lemmatized
    assert "fox" in keywords
    assert "dog" in keywords
    assert "brown" in keywords
    
    # Stop words and prepositions should be discarded
    assert "the" not in keywords
    assert "over" not in keywords
    
def test_tokenize_interests():
    interests = ["Artificial Intelligence", "Sports"]
    tokens = tokenize_interests(interests)
    
    # Validation of tokenization and lemmatization ("sports" -> "sport")
    assert "artificial" in tokens
    assert "intelligence" in tokens
    assert "sport" in tokens
    
def test_calculate_similarity():
    # Mock user weighted dictionary
    user_weighted_tokens = {"math": 1.0, "science": 1.5, "coding": 2.0}
    
    # Mock event tokens
    event_words = ["coding", "science", "art", "music"]
    
    # Coding TF (1/4) * 2.0 = 0.50
    # Science TF (1/4) * 1.5 = 0.375
    # Total Base Score = 0.875
    # Scaled (0.875 * 300) = 262.5 -> Capped at 100.0
    
    score = calculate_similarity(user_weighted_tokens, event_words)
    assert score == 100.0
    
    # 0% match validation
    score_zero = calculate_similarity({"sport": 1.0}, ["music", "art"])
    assert score_zero == 0.0
