import logging
import spacy
from prompt_generator.online_prompt import OnlineResearchPromptGenerator
from prompt_generator.meeting_prompt import MeetingPromptGenerator
from prompt_generator.default_prompt_generator import DefaultPromptGenerator



# Carregar o modelo de linguagem natural
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
        contexts = self.api_client.fetch_all_contexts()
        context_str = "\n".join([context['context'] for context in contexts])
        response = None

        if any(keyword in command.lower() for keyword in ["pesquise", "pesquisar", "procure"]):
            prompt_generator = OnlineResearchPromptGenerator()
            response = self.get_online_research_response(command)
        elif "contexto" in command.lower():
            prompt_generator = OnlineResearchPromptGenerator()
            response = self.get_project_response(command, context_str, meeting)
        elif any(keyword in command.lower() for keyword in ["faça resumo da reunião.", "tópicos da reunião", "resuma a reunião", "mostre os tópicos"]):
            prompt_generator = MeetingPromptGenerator()
            meeting = self.api_client.fetch_last_meeting()
            response = self.get_meeting_analysis_response(command, meeting)
        else:
            prompt_generator = DefaultPromptGenerator()
            response = self.handle_default_command(command, meeting)

        if response:
            question_embedding = self.question_answer_service.convert_text_to_embedding(command)
            answer_embedding = self.question_answer_service.convert_text_to_embedding(response)
            self.api_client.save_question_answer(command, question_embedding, response, answer_embedding)
            self.conversation_history.add_interaction(command, response)
            self.context_manager.add_context(command, response)

        return response

    def handle_default_command(self, command, meeting):
        question_embedding = self.question_answer_service.convert_text_to_embedding(command)
        similar_embeddings = self.api_client.find_similar_embeddings(question_embedding)
        context_str = self.api_client.fetch_all_contexts()
        for embedding in similar_embeddings:
            context_str += f"Pergunta: {embedding['question']}\nResposta: {embedding['answer']}\n"
        response = self.get_project_response(command, context_str, meeting)
        if response:
            answer_embedding = self.question_answer_service.convert_text_to_embedding(response)
            self.conversation_history.add_interaction(command, response)
        return response

    def get_online_research_response(self, command):
        prompt = OnlineResearchPromptGenerator().generate_prompt(command, "", "")
        return self.api_client.get_text_response(prompt, "", "")

    def get_meeting_analysis_response(self, command, meeting):
        prompt = MeetingPromptGenerator().generate_prompt(command, "", meeting)
        return self.api_client.get_text_response(prompt, "", meeting)
    
    def get_project_response(self, command, context_str, meeting):
        prompt = DefaultPromptGenerator().generate_prompt(command, context_str, meeting)
        return self.api_client.get_text_response(prompt, context_str, meeting)
