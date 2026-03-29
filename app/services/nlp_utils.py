import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

lemmatizer = WordNetLemmatizer()
ENGLISH_STOP_WORDS = set(stopwords.words('english'))

def extract_keywords(text: str, top_n: int = 15) -> str:
    """
    Takes raw event description text, tokenizes it, performs POS tagging
    to extract only Nouns and Adjectives, Lemmatizes them to root form,
    removes stopwords, and returns the top_n keywords.
    """
    if not text:
        return ""
        
    try:
        tokens = word_tokenize(text)
    except LookupError: # Fallback
        tokens = text.split()
        
    # Part of Speech Tagging (Requires original casing for best accuracy)
    try:
        pos_tags = nltk.pos_tag(tokens)
    except LookupError:
        pos_tags = [(t, 'NN') for t in tokens]
        
    filtered_lemmas = []
    
    # NN = Noun, singular | NNS = Noun, plural | NNP = Proper noun | JJ = Adjective
    allowed_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS']
    
    for word, tag in pos_tags:
        word_lower = word.lower().strip(string.punctuation)
        if tag in allowed_tags and word_lower and word_lower not in ENGLISH_STOP_WORDS and len(word_lower) > 2 and word_lower.isalpha():
            # Lemmatize the lowercase word
            lemma = lemmatizer.lemmatize(word_lower)
            filtered_lemmas.append(lemma)
            
    # Count frequencies
    word_counts = Counter(filtered_lemmas)
    
    # Get top_n most common semantic words
    top_words = [word for word, count in word_counts.most_common(top_n)]
    
    return ",".join(top_words)

def tokenize_interests(interests_list: list) -> list:
    """
    Takes a list of interest names and breaks them down into individual 
    lemmatized tokens.
    """
    all_tokens = []
    for interest in interests_list:
        try:
            tokens = word_tokenize(interest.lower())
        except LookupError:
            tokens = interest.lower().split()
            
        for w in tokens:
            w_clean = w.lower().strip(string.punctuation)
            if w_clean and w_clean.isalpha() and len(w_clean) > 2:
                all_tokens.append(lemmatizer.lemmatize(w_clean))
    
    return list(set(all_tokens))
