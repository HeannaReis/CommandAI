# config.py
import pyttsx3
import spacy
from collections import deque

class APIConfig:
    apiKey = "API_KEY"
    url = "https://gpt-templates.saiapplications.com"
    headers = {"X-Api-Key": apiKey}

# Inicialização do motor de texto para voz
engine = pyttsx3.init()

# Inicializa o contexto como uma deque para manter as últimas interações
recent_context = deque(maxlen=10)

# Inicialização do modelo de linguagem
nlp = spacy.load("pt_core_news_sm")
