import requests
import logging
import google.generativeai as genai

# Configure o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, similarity_url, save_url, model):
        self.similarity_url = similarity_url
        self.save_url = save_url
        self.model = model

    def get_text_response(self, prompt, context, feedback):
        try:
            # Gerando o conteúdo usando a nova API
            response = self.model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return prompt, response.text
            else:
                logger.error("Resposta inválida da API")
                return prompt, None
        except Exception as e:
            logger.error(f"Erro em get_text_response: {e}")
            return prompt, None

    def find_similar_embeddings(self, embedding):
        try:
            if hasattr(embedding, 'tolist'):
                embedding = embedding.tolist()
            data = embedding
            logger.info(f"Enviando dados para a API de embeddings similares: {data}")
            response = requests.post(f"{self.similarity_url}/api/question_answers/similar", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Erro em find_similar_embeddings: {e}")
            return []

    def save_question_answer(self, question, question_embedding, answer, answer_embedding):
        try:
            data = {
                "question": question,
                "questionEmbedding": question_embedding.tolist() if hasattr(question_embedding, 'tolist') else question_embedding,
                "answer": answer,
                "answerEmbedding": answer_embedding.tolist() if hasattr(answer_embedding, 'tolist') else answer_embedding
            }
            response = requests.post(self.save_url, json=data)
            response.raise_for_status()
            if response.status_code == 201:
                logger.info("Pergunta e resposta salvas com sucesso.")
            else:
                logger.warning(f"Falha ao salvar pergunta e resposta. Código de status: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Erro em save_question_answer: {e}")
