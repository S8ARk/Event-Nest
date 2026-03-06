import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# We assume punkt and stopwords have been downloaded per the outliers in Module 1.
# nltk.download('punkt')
# nltk.download('stopwords')

def extract_keywords(text: str, top_n: int = 15) -> str:
    """
    Takes raw event description text, tokenizes it, removes stopwords 
    and punctuation, and returns the top_n keywords as a comma-separated string.
    """
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    try:
        # Tokenize using NLTK
        tokens = word_tokenize(text)
    except LookupError:
        # Fallback if punkt isn't properly installed
        tokens = text.split()
        
    # Remove punctuation and stopwords
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    
    # Filter out short words, stopwords, and punctuation
    filtered_tokens = [
        word for word in tokens 
        if word not in stop_words 
        and word not in punctuation
        and len(word) > 2
        and word.isalpha()
    ]
    
    # Count frequencies
    word_counts = Counter(filtered_tokens)
    
    # Get top_n most common words
    top_words = [word for word, count in word_counts.most_common(top_n)]
    
    # Return as comma separated string for DB storage
    return ",".join(top_words)

def tokenize_interests(interests_list: list) -> list:
    """
    Takes a list of interest names (e.g. ['Artificial Intelligence', 'Sports'])
    and breaks them down into individual searchable NLTK token keywords.
    """
    all_tokens = []
    for interest in interests_list:
        try:
            tokens = word_tokenize(interest.lower())
        except LookupError:
            tokens = interest.lower().split()
            
        filtered = [w for w in tokens if w.isalpha() and len(w) > 2]
        all_tokens.extend(filtered)
        
    return list(set(all_tokens)) # Return unique tokens
