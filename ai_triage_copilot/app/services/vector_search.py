import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorSearch:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.descriptions = []

    def add_to_index(self, descriptions):
        embeddings = self.model.encode(descriptions)
        self.index.add(embeddings)
        self.descriptions.extend(descriptions)

    def search(self, query, k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        return [self.descriptions[i] for i in indices[0]]

vector_search = VectorSearch()
