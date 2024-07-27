pyaudio
pydub
pvporcupine
speechrecognizer
whisper
noisereduce
webrtcvad
sentence-transformers

# Função para criar o prompt
def create_prompt(command, context, feedback):
    return f"""
    Seu nome é [StefanAI].
    Você é um assistente virtual inteligente e utiliza [str_texto] para entender o que deve responder.
    
    Regras Gerais:
    - Responda de forma clara e concisa, evitando parecer cansativo.
    - Mantenha um tom natural e humano em suas respostas, sem títulos ou marcadores.
    - Responda em Formato JSON

    Regras de Contexto:
    - Utilize [str_contexto] para responder perguntas relacionadas ao projeto.
    - Se [str_texto] não tiver relação com [str_contexto] ou [str_feedback], utilize seu banco de dados pessoal para responder.

    Regras de Feedback:
    - Para perguntas que envolvem "Análise de Feedback", utilize [str_feedback] para fornecer uma visão geral resumida.
    - Apenas gere a saída de feedback se [str_texto] conter as palavras "Faça, analise, Sentimento, Feedbacks".
        Responda no formato JSON com as chaves: "feedback_description", "sentiment" e "score".
        - Descrição do feedback
        - Sentimento: 5 estrelas
        - Pontuação: 0.90

    Regras de Pesquisa e Ação:
    - Se [str_texto] solicitar pesquisa online ou uma ação específica, faça uma busca online.
    - Diferencie claramente entre perguntas do escopo do projeto e outras solicitações.

    Exemplo de Diferenciação:
    - Para comandos de escopo do projeto: "Qual é o status atual do projeto?"
    - Para ações específicas: "Pesquise online as melhores práticas para implementação de SAP Ariba."

    [str_texto]: {command}
    [str_contexto]: {context}
    [str_feedback]: {feedback}
    """




Este bloco é onde você insere o código Mermaid para desenhar o diagrama. O GitHub detecta a palavra-chave `mermaid` e renderiza o diagrama automaticamente.

### Estrutura do Diagrama em Mermaid

O diagrama mostra a estrutura das tabelas e seus relacionamentos:

- **USERS**: Tabela com informações sobre os usuários.
- **NEWS**: Tabela com notícias.
- **TRANSCRIPTIONS**: Tabela para armazenar transcrições associadas aos usuários.
- **FEEDBACKS**: Tabela para feedbacks dados pelos usuários.
- **FAQ**: Tabela para perguntas e respostas frequentes.
- **CONTEXT**: Tabela para contextos criados pelos usuários.

### Relações Entre Tabelas

- **USERS** pode criar várias **TRANSCRIPTIONS**, **FEEDBACKS** e **CONTEXT**.
- **TRANSCRIPTIONS** pertence a um único **USERS**.
- **FEEDBACKS** pertence a um único **USERS**.
- **CONTEXT** pertence a um único **USERS**.

### Exemplos de Adição de Texto Explicativo

Você pode adicionar mais explicações ou descrições sobre o diagrama conforme necessário. Por exemplo:

```markdown
## Entity-Relationship Diagram

The following diagram illustrates the relationships between different entities in the system:

- **USERS** table stores user information.
- **NEWS** table stores news articles.
- **TRANSCRIPTIONS** table stores transcriptions created by users.
- **FEEDBACKS** table stores feedback provided by users.
- **FAQ** table stores frequently asked questions and their answers.
- **CONTEXT** table stores context information created by users.

```mermaid
erDiagram
  USERS {
      id INT PK "Primary Key"
      name VARCHAR "Name"
      email VARCHAR "Email"
      password VARCHAR "Password"
  }

  NEWS {
      id INT PK "Primary Key"
      title VARCHAR "Title"
      content TEXT "Content"
      publication_date DATE "Publication Date"
  }

  TRANSCRIPTIONS {
      id INT PK "Primary Key"
      user_id INT FK "Foreign Key to USERS"
      content TEXT "Content"
      date TIMESTAMP "Date"
  }

  FEEDBACKS {
      id INT PK "Primary Key"
      user_id INT FK "Foreign Key to USERS"
      sentiment VARCHAR "Sentiment"
      score INT "Score"
  }

  FAQ {
      id INT PK "Primary Key"
      question TEXT "Question"
      answer TEXT "Answer"
  }

  CONTEXT {
      id INT PK "Primary Key"
      user_id INT FK "Foreign Key to USERS"
      context TEXT "Context"
  }

  USERS ||--o{ TRANSCRIPTIONS : "has"
  USERS ||--o{ FEEDBACKS : "gives"
  USERS ||--o{ CONTEXT : "creates"
  TRANSCRIPTIONS }o--|| USERS : "belongs to"
  FEEDBACKS }o--|| USERS : "belongs to"
  CONTEXT }o--|| USERS : "belongs to"


CREATE TABLE embeddings_reunioes (
    id SERIAL PRIMARY KEY,
    conteudo TEXT NOT NULL, -- Texto original da reunião
    embedding BYTEA NOT NULL, -- Embedding armazenado como array de bytes
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE embeddings_perguntas_respostas (
    id SERIAL PRIMARY KEY,
    pergunta TEXT NOT NULL, -- Texto da pergunta
    resposta TEXT NOT NULL, -- Texto da resposta
    embedding BYTEA NOT NULL, -- Embedding armazenado como array de bytes
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
