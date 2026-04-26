import gensim.downloader as api

def load_model():
    print("Loading Word2Vec model (this may take time)...")
    model = api.load("word2vec-google-news-300")
    print("Model loaded successfully!")
    return model

def test_model(model):
    print("\n--- Testing Model ---")
    
    # Similar words
    word = "king"
    print(f"\nTop similar words to '{word}':")
    for w, score in model.most_similar(word, topn=5):
        print(f"{w} : {score:.4f}")
    
    # Word similarity
    similarity = model.similarity("king", "queen")
    print(f"\nSimilarity between 'king' and 'queen': {similarity:.4f}")
    
    # Analogy
    result = model.most_similar(positive=["king", "woman"], negative=["man"], topn=1)
    print("\nAnalogy: king - man + woman =")
    print(result)

if __name__ == "__main__":
    model = load_model()
    test_model(model)