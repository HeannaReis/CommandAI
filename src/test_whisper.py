from transformers import pipeline
from common_paths import AUDIO_INPUT_PATH, TRANSCRIPTION_OUTPUT_PATH

# Função para ler a transcrição de um arquivo
def read_transcription(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

# Função para converter a pontuação em estrelas
def score_to_stars(score):
    if score >= 0.75:
        return 5
    elif score >= 0.55:
        return 4
    elif score >= 0.35:
        return 3
    elif score >= 0.15:
        return 2
    else:
        return 1

# Inicializar o pipeline de análise de sentimento
sentiment_pipeline = pipeline("sentiment-analysis", model="neuralmind/bert-base-portuguese-cased")

# Caminho para o arquivo de transcrição
file_path = TRANSCRIPTION_OUTPUT_PATH / 'feedback.txt'

# Ler a transcrição
lines = read_transcription(file_path)

# Analisar sentimento para cada feedback
for line in lines:
    sentiment = sentiment_pipeline(line.strip())
    score = sentiment[0]['score']
    stars = score_to_stars(score)
    
    # Ajuste manual para feedbacks com aspectos positivos e negativos
    if any(word in line.lower() for word in ["mas", "porém", "no entanto"]):
        stars = max(1, stars - 1)  # Reduz uma estrela se houver contradição
    
    # Ajuste adicional baseado em palavras-chave
    positive_keywords = ["excelente", "ótimo", "perfeito", "rápido", "eficiente", "satisfeito", "clara", "eficaz", "bom trabalho"]
    negative_keywords = ["ruim", "péssimo", "horrível", "poderia", "não resolveu", "insatisfatória", "confusa", "inadequado", "lento", "não houve seguimento", "não atendeu", "não funcionou", "demorado"]
    
    positive_count = sum(word in line.lower() for word in positive_keywords)
    negative_count = sum(word in line.lower() for word in negative_keywords)
    
    # Ajuste de estrelas baseado na contagem de palavras-chave
    if positive_count > negative_count:
        stars = min(5, stars + 1)
    elif negative_count > positive_count:
        stars = max(1, stars - 1)
    
    print(f"Texto: {line.strip()}")
    print(f"Sentimento: {stars} estrelas")
    print(f"Pontuação: {score:.2f}")
    print('---')
