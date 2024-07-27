import speech_recognition as sr
from translate import Translator

def ouvir_e_traduzir():
    # Inicializa o reconhecedor de fala
    recognizer = sr.Recognizer()

    # Configura o tradutor
    translator = Translator(to_lang="en", from_lang="pt")

    # Usa o microfone como fonte de áudio
    with sr.Microphone() as source:
        print("Diga algo em português...")

        while True:
            try:
                # Escuta o áudio do microfone
                audio = recognizer.listen(source)
                
                # Reconhece a fala usando o Google Web Speech API
                texto_portugues = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {texto_portugues}")

                # Traduz o texto para o inglês
                traducao = translator.translate(texto_portugues)
                print(f"Tradução para o inglês: {traducao}")

            except sr.UnknownValueError:
                print("Não foi possível entender o áudio")
            except sr.RequestError as e:
                print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")

if __name__ == "__main__":
    try:
        ouvir_e_traduzir()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
