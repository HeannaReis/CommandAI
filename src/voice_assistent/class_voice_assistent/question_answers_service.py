import requests
import numpy as np
from sentence_transformers import SentenceTransformer

class QuestionAnswerService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(model_name)

    def convert_text_to_embedding(self, text):
        embedding = self.embedding_model.encode(text)
        print(f"Embedding gerado para '{text}': {embedding[0]:.16f}") # Adicionado para verificar o embedding gerado
        return embedding
