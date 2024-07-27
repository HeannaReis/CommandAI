import os
from dotenv import load_dotenv
from groq import Groq

# Carregar variáveis do arquivo .env
load_dotenv()

# Recuperar a chave da API
api_key = os.getenv("GROQ_API_KEY")

# Verificar se a chave da API foi carregada corretamente
if not api_key:
    raise ValueError("API Key is missing. Please set the GROQ_API_KEY in the .env file.")

# Configurar o cliente com a chave da API
client = Groq(api_key=api_key)

# Criação da conclusão do chat
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Boa tarde, sabe dizer que dia é hoje ?",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
