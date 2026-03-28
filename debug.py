import nltk
from nltk.tokenize import word_tokenize
text = "The quick brown fox jumps over the lazy dog. The fox is fast."
tokens = word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)
print("TAGS:", pos_tags)
