import speech_recognition as sr

class VoiceCommandHandler:
    def capture_voice_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Por favor, fale o seu comando:")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Áudio capturado com sucesso.")
                command = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {command}")
                return command
            except sr.WaitTimeoutError:
                print("Tempo de espera expirado. Nenhum áudio detectado.")
                return None
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio.")
                return None
            except sr.RequestError as e:
                print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
                return None
