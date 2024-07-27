import logging
import requests
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

class APIClient:
    def __init__(self, similarity_url, save_url, model):
        self.similarity_url = similarity_url
        self.save_url = save_url
        self.model = model

    def get_text_response(self, prompt, context, meeting):
        try:
            logging.debug(f"Enviando prompt para a API GPT: {prompt}")
            response_text = self.model.generate_content(prompt, context, meeting)
            return response_text
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return None

    def find_similar_embeddings(self, embedding):
        try:
            if hasattr(embedding, 'tolist'):
                embedding = embedding.tolist()
            data = embedding
            response = requests.post(f"{self.similarity_url}/api/question_answers/similar", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Erro em find_similar_embeddings: {e}")
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
                logging.info("Pergunta e resposta salvas com sucesso.")
            else:
                logging.warning(f"Falha ao salvar pergunta e resposta. Código de status: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Erro em save_question_answer: {e}")

    def fetch_all_contexts(self):
        try:
            response = requests.get("http://localhost:8081/api/contexts/all")
            if response.status_code == 200:
                data = response.json()
                contexts = data.get('contexts', [])
                if isinstance(contexts, list):
                    logging.info(f"Contexto obtido da API: {contexts}")
                    return contexts
                else:
                    logging.error(f"Erro: 'contexts' não é uma lista. Dados retornados: {data}")
                    return []
            else:
                logging.error(f"Erro ao acessar a API de contextos: {response.status_code}, {response.text}")
                return []
        except requests.RequestException as e:
            logging.error(f"Erro ao fazer requisição para a API de contextos: {e}")
            return []

    def fetch_last_meeting(self):
        try:
            response = requests.get("http://localhost:8081/api/meetings/last")
            if response.status_code == 200:
                data = response.json()
                transcription_text = data.get('transcriptionText', "")
                if isinstance(transcription_text, str):
                    logging.info(f"Texto da transcrição obtido da API: {transcription_text}")
                    return transcription_text
                else:
                    logging.error(f"Erro: 'transcriptionText' não é uma string. Dados retornados: {data}")
                    return ""
            else:
                logging.error(f"Erro ao acessar a API de reuniões: {response.status_code}, {response.text}")
                return ""
        except requests.RequestException as e:
            logging.error(f"Erro ao fazer requisição para a API de reuniões: {e}")
            return ""
