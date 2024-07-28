import spacy
from prompt_generator.online_prompt import OnlineResearchPromptGenerator
from prompt_generator.meeting_prompt import MeetingPromptGenerator
from prompt_generator.default_prompt_generator import DefaultPromptGenerator

# Carregar o modelo de linguagem natural
nlp = spacy.load("pt_core_news_sm")
class CommandInterpreter:
    def __init__(self, api_client, question_answer_service, conversation_history, context_manager):
        self.api_client = api_client
        self.question_answer_service = question_answer_service
        self.conversation_history = conversation_history
        self.context_manager = context_manager

    def interpret_command(self, command, meeting):
        print(f"Interpretando comando: {command}")
        contexts = self.api_client.fetch_all_contexts()
        context_str = "\n".join([context['context'] for context in contexts])
        response = None

        # Gerar embedding para a pergunta e buscar embeddings similares
        question_embedding = self.question_answer_service.convert_text_to_embedding(command)
        similar_embeddings = self.api_client.find_similar_embeddings(question_embedding)
        for embedding in similar_embeddings:
            context_str += f"Pergunta: {embedding['question']}\nResposta: {embedding['answer']}\n"

        if any(keyword in command.lower() for keyword in ["pesquise", "pesquisar", "procure"]):
            print(f"Comando identificado como pesquisa online.")
            response = self.get_online_research_response(command, context_str)
        elif "contexto" in command.lower():
            print(f"Comando identificado como busca de contexto.")
            response = self.get_project_response(command, context_str, meeting)
        elif any(keyword in command.lower() for keyword in ["faça resumo da reunião.", "tópicos da reunião", "resuma a reunião", "mostre os tópicos"]):
            print(f"Comando identificado como análise de reunião.")
            meeting = self.api_client.fetch_last_meeting()
            response = self.get_meeting_analysis_response(command, meeting)
        else:
            print(f"Comando identificado como comando padrão.")
            response = self.handle_default_command(command, meeting)

        if response:
            answer_embedding = self.question_answer_service.convert_text_to_embedding(response)
            self.api_client.save_question_answer(command, question_embedding, response, answer_embedding)
            self.conversation_history.add_interaction(command, response)
            self.context_manager.add_context(command, response)

        return response

    def handle_default_command(self, command, meeting):
        print(f"Tratando comando padrão: {command}")
        context_str = self.api_client.fetch_all_contexts()
        response = self.get_project_response(command, context_str, meeting)
        if response:
            answer_embedding = self.question_answer_service.convert_text_to_embedding(response)
            self.conversation_history.add_interaction(command, response)
        return response

    def get_online_research_response(self, command, context_str):
        print(f"Gerando prompt de pesquisa online.")
        prompt = OnlineResearchPromptGenerator().generate_prompt(command, context_str, "")
        return self.api_client.get_text_response(prompt, context_str, "")

    def get_meeting_analysis_response(self, command, meeting):
        print(f"Gerando prompt de análise de reunião.")
        prompt = MeetingPromptGenerator().generate_prompt(command, "", meeting)
        return self.api_client.get_text_response(prompt, "", meeting)
    
    def get_project_response(self, command, context_str, meeting):
        print(f"Gerando prompt de projeto.")
        prompt = DefaultPromptGenerator().generate_prompt(command, context_str, meeting)
        return self.api_client.get_text_response(prompt, context_str, meeting)
