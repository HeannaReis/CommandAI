
from common_paths import TRANSCRIPTION_OUTPUT_PATH, EMBEDDING_OUTPUT_PATH
from sentence_transformers import SentenceTransformer
import numpy as np

# Carregar o modelo de embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def process_transcription_file(transcription_file_path):
    try:
        # Ler a transcrição do arquivo de texto
        with open(transcription_file_path, 'r', encoding='utf-8') as f:
            transcription_text = f.read()

        # Gerar o embedding da transcrição
        embedding = embedding_model.encode(transcription_text)

        # Salvar o embedding em um arquivo .npy
        embedding_file_path = EMBEDDING_OUTPUT_PATH / transcription_file_path.with_suffix('.npy').name
        np.save(embedding_file_path, embedding)
        print(f"Embedding salvo em: {embedding_file_path}")

    except Exception as e:
        print(f"Erro ao processar o arquivo {transcription_file_path}: {e}")

# Listar todos os arquivos de transcrição no diretório de saída
transcription_files = list(TRANSCRIPTION_OUTPUT_PATH.glob('*.txt'))

# Verificar se existem arquivos de transcrição no diretório de saída
if not transcription_files:
    print(f"Não foram encontrados arquivos de transcrição no diretório {TRANSCRIPTION_OUTPUT_PATH}.")
else:
    for transcription_file_path in transcription_files:
        if transcription_file_path.is_file():
            print(f"Processando arquivo: {transcription_file_path}")
            process_transcription_file(transcription_file_path)