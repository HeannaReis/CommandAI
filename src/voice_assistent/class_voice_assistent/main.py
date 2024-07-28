import os
from context_manager import ContextManager
from api_client import APIClient
from command_interpreter import CommandInterpreter
from text_command_hendler import TextCommandHandler
from text_processor import TextProcessor
from text_to_speech import TextToSpeech
from voice_command_hendler import VoiceCommandHandler
from question_answers_service import QuestionAnswerService
from conversation_history import ConversationHistory
from gpt_communication.gemini_gpt import GenerativeModelHandler

class MainApp:
    def __init__(self, model):
        self.voice_handler = VoiceCommandHandler()
        self.text_handler = TextCommandHandler()
        self.tts = TextToSpeech()
        self.text_processor = TextProcessor()
        self.api_client = APIClient(similarity_url="http://localhost:8081", save_url="http://localhost:8081/api/question_answers/save", model=model)
        self.context_manager = ContextManager()
        self.question_answer_service = QuestionAnswerService()
        self.conversation_history = ConversationHistory()
        self.command_interpreter = CommandInterpreter(self.api_client, self.question_answer_service, self.conversation_history, self.context_manager)

    def run(self):
        meeting = ""
        while True:
            try:
                input_type = input("Você quer usar voz ou texto? (v/t): ").strip().lower()
                if input_type == 'v':
                    command = self.voice_handler.capture_voice_command()
                elif input_type == 't':
                    command = self.text_handler.capture_text_command()
                else:
                    print("Opção inválida. Por favor, escolha 'v' para voz ou 't' para texto.")
                    continue

                if command:
                    # Log da pergunta antes de enviar para o interpretador
                    print(f"Pergunta recebida: {command}")
                    text_response = self.command_interpreter.interpret_command(command, meeting)
                    if text_response:
                        print(f"Resposta: {text_response}")
                        self.tts.speak_text(text_response)
                        self.context_manager.add_context(command, text_response)
                else:
                    print("Nenhum comando detectado. Aguardando novamente...")
                    continue
            except Exception as e:
                print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    model = GenerativeModelHandler('gemini-1.5-flash')
    app = MainApp(model)
    app.run()