import logging
import requests
import spacy
import os
import webbrowser
from prompt import create_prompt

# Carregar o modelo de linguagin natural
nlp = spacy.load("pt_core_news_sm")

logging.basicConfig(
    level=logging.WARNING,  # Exibe apenas avisos, erros e críticos
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

class CommandInterpreter:
    def __init__(self, api_client, question_answer_service, conversation_history, context_manager):
        self.api_client = api_client
        self.question_answer_service = question_answer_service
        self.conversation_history = conversation_history
        self.context_manager = context_manager

    def interpret_command(self, command, meeting):
        # Atualiza o contexto com base na API antes de elaborar a resposta
        contexts = self.api_client.fetch_all_contexts()

        doc = nlp(command)
        response = None  # Inicializa a variável de resposta

        if "abrir" in command:
            if "navegador" in command:
                webbrowser.open("http://www.google.com")
                response = "Abrindo navegador"
            elif "arquivo" in command or "pasta" in command:
                for token in doc:
                    if token.pos_ == "NOUN":
                        path = token.text
                        if os.path.exists(path):
                            os.startfile(path)
                            response = f"Abrindo {path}"
                        else:
                            response = f"Arquivo ou pasta {path} não encontrado"
        elif any(keyword in command.lower() for keyword in ["pesquise", "pesquisar", "procure"]):
            response = self.get_online_research_response(command)
        elif "contexto" in command.lower():
            contexts = self.api_client.fetch_all_contexts()
            context_str = "\n".join([context['context'] for context in contexts])
            response = self.get_project_response(command, context_str, meeting)
        elif any(keyword in command.lower() for keyword in ["faça resumo da reunião.", "tópicos da reunião", "resuma a reunião", "mostre os tópicos"]):
            meeting = self.api_client.fetch_last_meeting()
            response = self.get_meeting_analysis_response(command, meeting)
        else:
            response = self.handle_default_command(command, meeting)

        # Gera embeddings e salva a pergunta e resposta, independentemente do comando
        if response:
            question_embedding = self.question_answer_service.convert_text_to_embedding(command)
            answer_embedding = self.question_answer_service.convert_text_to_embedding(response)
            self.api_client.save_question_answer(command, question_embedding, response, answer_embedding)
            self.conversation_history.add_interaction(command, response)
            self.context_manager.add_context(command, response)

        return response


    def handle_open_command(self, doc):
        if "navegador" in doc.text:
            webbrowser.open("http://www.google.com")
            return "Abrindo navegador"
        elif "arquivo" in doc.text or "pasta" in doc.text:
            for token in doc:
                if token.pos_ == "NOUN":
                    path = token.text
                    if os.path.exists(path):
                        os.startfile(path)
                        return f"Abrindo {path}"
                    else:
                        return f"Arquivo ou pasta {path} não encontrado"

    def handle_meeting_command(self, command):
        meeting = self.api_client.fetch_last_meeting()
        return self.get_meeting_analysis_response(command, meeting)

    def handle_summary_command(self, command):
        meeting = self.api_client.fetch_last_meeting()
        return self.get_meeting_analysis_response(command, meeting)

    def handle_research_command(self, command):
        prompt = create_prompt(command, "", "")
        return self.api_client.get_text_response(prompt, "", "")

    def handle_context_command(self, command):
        contexts = self.api_client.fetch_all_contexts()
        context_str = "\n".join([context['context'] for context in contexts])
        return self.get_project_response(command, context_str, "")

    def handle_default_command(self, command, meeting):
        question_embedding = self.question_answer_service.convert_text_to_embedding(command)
        logging.info(f"Embedding da pergunta (numpy array): {question_embedding}")

        question_embedding_list = [format(num, ".8e") for num in question_embedding]
        logging.info(f"Embedding da pergunta (lista): {question_embedding_list}")

        similar_embeddings = self.api_client.find_similar_embeddings(question_embedding_list)
        logging.info(f"Embeddings similares: {similar_embeddings}")

        context_str = self.api_client.fetch_all_contexts()
        for embedding in similar_embeddings:
            context_str += f"Pergunta: {embedding['question']}\nResposta: {embedding['answer']}\n"

        response = self.get_project_response(command, context_str, meeting)
        if response:
            answer_embedding = self.question_answer_service.convert_text_to_embedding(response)
            logging.info(f"Embedding da resposta: {answer_embedding}")
            self.api_client.save_question_answer(command, question_embedding, response, answer_embedding)
            self.conversation_history.add_interaction(command, response)
        return response

    def get_meeting_analysis_response(self, command, meeting):
        prompt = create_prompt(command, "", meeting)
        return self.api_client.get_text_response(prompt, "", meeting)
    
    def get_online_research_response(self, command):
        prompt = create_prompt(command, "", "")
        return self.api_client.get_text_response(prompt, "", "")
    
    def get_project_response(self, command, context_str, meeting):
        prompt = create_prompt(command, context_str, meeting)
        logging.info(f"Prompt enviado para a API GPT: {prompt}")
        return self.api_client.get_text_response(prompt, context_str, meeting)
