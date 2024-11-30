from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """Generate embeddings for patterns."""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def generate(self, text: str) -> list:
        """Generate embeddings for text."""
        return self.model.encode(text).tolist() 