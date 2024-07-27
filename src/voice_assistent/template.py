import speech_recognition as sr
import requests
import pyttsx3
import re
from collections import deque
import spacy
import os
import webbrowser
from voice_assistent.prompt import create_prompt

# Configurações da API
apiKey = "6UlOOoY/kkmprunma/qNDg"
url = "https://gpt-templates.saiapplications.com"
headers = {"X-Api-Key": apiKey}

# Inicialização do motor de texto para voz
engine = pyttsx3.init()

# Inicializa o contexto como uma deque para manter as últimas interações
recent_context = deque(maxlen=10)

# Inicialização do modelo de linguagem
nlp = spacy.load("pt_core_news_sm")

# Função para capturar e processar comandos de voz
def capture_voice_command():
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

# Função para capturar comandos de texto
def capture_text_command():
    command = input("Digite o seu comando: ")
    return command

# Função para converter texto em fala
def speak_text(text):
    if isinstance(text, dict):
        text = extract_values_from_json(text)  # Extrai os valores do dicionário
    cleaned_text = clean_text(text)
    engine.say(cleaned_text)
    engine.runAndWait()

# Função para remover caracteres especiais do texto
def clean_text(text):
    return re.sub(r'[\*\_]', '', text)

# Função para extrair valores do JSON
def extract_values_from_json(data):
    if isinstance(data, dict):
        return ' '.join([str(value) for value in data.values()])
    elif isinstance(data, list):
        return ' '.join([extract_values_from_json(item) for item in data])
    return str(data)

def get_text_response(prompt, context, feedback):
    data = {
        "inputs": {
            "str_texto": prompt,
            "str_contexto": context,
            "str_feedback": feedback
        }
    }
    print(f"Enviando dados para a API: {data}")
    try:
        response = requests.post(f"{url}/api/templates/6691e223802f95c2b394a8bd/execute", json=data, headers=headers)
        print(f"Status da resposta: {response.status_code}")
        if response.status_code == 200:
            try:
                response_data = response.html()  # Tente converter a resposta para JSON
                print("Resposta HTML recebida.")
                return extract_values_from_json(response_data)  # Extrai os valores do JSON
            except ValueError:
                print("A resposta não está no formato JSON esperado. Tratando como texto simples.")
                return response.text  # Retorna o texto bruto da resposta
        else:
            print(f"Erro ao acessar a API: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Erro ao fazer requisição para a API: {e}")
        return None

# Função para extrair valores do JSON
def extract_values_from_json(data):
    if isinstance(data, dict):
        return ' '.join([str(value) for value in data.values()])
    elif isinstance(data, list):
        return ' '.join([extract_values_from_json(item) for item in data])
    return str(data)


# Função para consultar todos os contextos da API
def fetch_all_contexts():
    try:
        response = requests.get("http://localhost:8081/contexts/all")
        # Verifica o status da resposta
        if response.status_code == 200:
            data = response.json()  # Obtemos o JSON completo

            # Imprime o JSON completo para verificar o retorno bruto
            print(f"Dados brutos da API: {data}")

            # Acessa a lista de contextos e imprime o tipo de dados
            contexts = data.get('contexts', [])
            print(f"Tipo de dados de 'contexts': {type(contexts)}")
            
            if isinstance(contexts, list):  # Verificamos se é uma lista
                context_str = "\n".join([context['context'] for context in contexts])
                print(f"Contexto obtido da API: {context_str}")  # Adiciona um print para verificar o contexto
                return contexts  # Retorna a lista completa de contextos
            else:
                print(f"Erro: 'contexts' não é uma lista. Dados retornados: {data}")
                return []
        else:
            print(f"Erro ao acessar a API de contextos: {response.status_code}, {response.text}")
            return []
    except requests.RequestException as e:
        print(f"Erro ao fazer requisição para a API de contextos: {e}")
        return []

# Função para interpretar comandos e delegar tarefas
def interpret_command(command, feedback):
    # Atualiza o contexto com base na API antes de elaborar a resposta
    contexts = fetch_all_contexts()
    
    doc = nlp(command)
    if "abrir" in command:
        if "navegador" in command:
            webbrowser.open("http://www.google.com")
            return "Abrindo navegador"
        elif "arquivo" in command or "pasta" in command:
            # Extraia o nome do arquivo ou pasta do comando
            for token in doc:
                if token.pos_ == "NOUN":
                    path = token.text
                    if os.path.exists(path):
                        os.startfile(path)
                        return f"Abrindo {path}"
                    else:
                        return f"Arquivo ou pasta {path} não encontrado"
    elif any(keyword in command.lower() for keyword in ["faça análise", "sentimento", "feedbacks", "feedback"]):
        return get_feedback_analysis_response(command, feedback)
    elif any(keyword in command.lower() for keyword in ["pesquise", "pesquisar", "procure"]):
        return get_online_research_response(command)
    else:
        context_str = "\n".join([context['context'] for context in contexts])  # Converter o contexto para string
        return get_project_response(command, context_str, feedback)

# Função para responder perguntas sobre o projeto
def get_project_response(command, context, feedback):
    prompt = create_prompt(command, context, feedback)
    print(f"Prompt enviado para a API GPT: {prompt}")  # Adiciona um print para verificar o prompt
    return get_text_response(prompt, context, feedback)

# Função para fazer pesquisas online
def get_online_research_response(command):
    prompt = create_prompt(command, "", "")
    return get_text_response(prompt, "", "")

# Função para análise de feedbacks
def get_feedback_analysis_response(command, feedback):
    prompt = create_prompt(command, "", feedback)
    return get_text_response(prompt, "", feedback)

# Loop principal para interação contínua, incluindo o contexto
def main():
    feedback = ""  # Inicializa o feedback como uma string vazia
    while True:
        input_type = input("Você quer usar voz ou texto? (v/t): ").strip().lower()
        if input_type == 'v':
            command = capture_voice_command()
        elif input_type == 't':
            command = capture_text_command()
        else:
            print("Opção inválida. Por favor, escolha 'v' para voz ou 't' para texto.")
            continue

        if command:
            text_response = interpret_command(command, feedback)
            if text_response:
                print(f"Resposta: {text_response}")
                speak_text(text_response)
                # Adiciona a interação recente ao contexto
                recent_context.append((command, text_response))
        else:
            print("Nenhum comando detectado. Aguardando novamente...")
            continue

if __name__ == "__main__":
    main()
