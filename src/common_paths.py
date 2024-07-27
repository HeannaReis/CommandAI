from pathlib import Path

# Diretório atual do script
ROOT_PATH = Path(__file__).resolve().parent
print(ROOT_PATH)

# Definição dos caminhos comuns
VIDEO_INPUT_PATH = ROOT_PATH / 'assets' / 'video'
AUDIO_INPUT_PATH = ROOT_PATH / 'assets' / 'audio'
AUDIO_OUTPUT_PATH = ROOT_PATH / 'assets' / 'audio'
TRANSCRIPTION_OUTPUT_PATH = ROOT_PATH / 'data'
EMBEDDING_OUTPUT_PATH = ROOT_PATH / 'data'

# Função para criar diretórios se não existirem
def create_directories():
    VIDEO_INPUT_PATH.mkdir(parents=True, exist_ok=True)
    AUDIO_INPUT_PATH.mkdir(parents=True, exist_ok=True)
    AUDIO_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTION_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Criação dos diretórios
create_directories()
