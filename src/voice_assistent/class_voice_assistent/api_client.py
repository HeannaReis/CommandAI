import requests


class APIClient:
    def __init__(self, similarity_url, save_url, model):
        self.similarity_url = similarity_url
        self.save_url = save_url
        self.model = model

    def get_text_response(self, prompt, context, meeting):
        try:
            print(f"Enviando prompt para a API Gemini")
            response_text = self.model.generate_content(prompt, context, meeting)
            print(response_text)
            return response_text
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None

    def find_similar_embeddings(self, embedding):
        try:
            print(f"Buscando embeddings similares para: {embedding}")
            if hasattr(embedding, 'tolist'):
                embedding = embedding.tolist()
            data = embedding
            response = requests.post(f"{self.similarity_url}/api/question_answers/similar", json=data)
            response.raise_for_status()
            similar_embeddings = response.json()
            print(f"Embeddings similares encontrados: {similar_embeddings}")
            return similar_embeddings
        except requests.RequestException as e:
            print(f"Erro em find_similar_embeddings: {e}")
            return []

    def save_question_answer(self, question, question_embedding, answer, answer_embedding):
        try:
            # Converter embeddings de numpy arrays para listas
            if hasattr(question_embedding, 'tolist'):
                question_embedding = question_embedding.tolist()
            if hasattr(answer_embedding, 'tolist'):
                answer_embedding = answer_embedding.tolist()
            
            data = {
                "question": question,
                "questionEmbedding": question_embedding,
                "answer": answer,
                "answerEmbedding": answer_embedding
            }
            
            response = requests.post(self.save_url, json=data)
            response.raise_for_status()
            if response.status_code == 201:
                print("Pergunta e resposta salvas com sucesso.")
            else:
                print(f"Falha ao salvar pergunta e resposta. Código de status: {response.status_code}")
        except requests.RequestException as e:
            print(f"Erro em save_question_answer: {e}")


    def fetch_all_contexts(self):
        try:
            response = requests.get("http://localhost:8081/api/contexts/all")
            if response.status_code == 200:
                data = response.json()
                contexts = data.get('contexts', [])
                if isinstance(contexts, list):
                    print(f"Contexto obtido da API: {contexts}")
                    return contexts
                else:
                    print(f"Erro: 'contexts' não é uma lista. Dados retornados: {data}")
                    return []
            else:
                print(f"Erro ao acessar a API de contextos: {response.status_code}, {response.text}")
                return []
        except requests.RequestException as e:
            print(f"Erro ao fazer requisição para a API de contextos: {e}")
            return []

    def fetch_last_meeting(self):
        try:
            response = requests.get("http://localhost:8081/api/meetings/last")
            if response.status_code == 200:
                data = response.json()
                transcription_text = data.get('transcriptionText', "")
                if isinstance(transcription_text, str):
                    print(f"Texto da transcrição obtido da API: {transcription_text}")
                    return transcription_text
                else:
                    print(f"Erro: 'transcriptionText' não é uma string. Dados retornados: {data}")
                    return ""
            else:
                print(f"Erro ao acessar a API de reuniões: {response.status_code}, {response.text}")
                return ""
        except requests.RequestException as e:
            print(f"Erro ao fazer requisição para a API de reuniões: {e}")
            return ""
