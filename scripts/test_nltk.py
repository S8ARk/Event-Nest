import nltk
print("Starting explicit NLTK downloads...")
dependencies = ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']
for dep in dependencies:
    print(f"Checking/Downloading: {dep}")
    nltk.download(dep, quiet=False)
print("Finished.")
