import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

class GenerativeModelHandler:
    def __init__(self, model_name: str):
        self.model_name: str = model_name
        self.model: Optional[genai.GenerativeModel] = None
        self.api_key: Optional[str] = None
        self._load_env_variables()
        self._configure_api()
        self._initialize_model()

    def _load_env_variables(self) -> None:
        """Carregar variáveis do arquivo .env"""
        load_dotenv()
        self.api_key = os.getenv('API_KEY_GEMINI')
        if not self.api_key:
            raise ValueError("API Key não encontrada nas variáveis de ambiente")

    def _configure_api(self) -> None:
        """Configurar a chave da API"""
        genai.configure(api_key=self.api_key)

    def _initialize_model(self) -> None:
        """Inicializar o modelo generativo"""
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Erro ao inicializar o modelo: {e}")

    def generate_content(self, prompt: str, context: str, meeting: str) -> str:
        """Gerar conteúdo com base no prompt, contexto e reunião"""
        try:
            # Supondo que a API espera um dicionário com os parâmetros
            request_data = f'''
                "prompt": {prompt},
                "context": {context},
                "meeting": {meeting}
            '''
            logging.debug(f"Enviando requisição para a API GenAI: {request_data}")

            response = self.model.generate_content(request_data)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar conteúdo: {e}")