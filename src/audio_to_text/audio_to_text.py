import whisper
from common_paths import AUDIO_INPUT_PATH, TRANSCRIPTION_OUTPUT_PATH

model = whisper.load_model("base")

def process_audio_file(audio_file_path):
    try:
        result = model.transcribe(str(audio_file_path))

        output_file_path = TRANSCRIPTION_OUTPUT_PATH / audio_file_path.with_suffix('.wav').name

        with open(output_file_path.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"Transcrição salva em: {output_file_path.with_suffix('.txt')}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {audio_file_path}: {e}")

# Listar todos os arquivos de áudio no diretório de entrada
audio_files = list(AUDIO_INPUT_PATH.glob('*'))

# Verificar se existem arquivos de áudio no diretório de entrada
if not audio_files:
    print(f"Não foram encontrados arquivos de áudio no diretório {AUDIO_INPUT_PATH}.")
else:
    for audio_file_path in audio_files:
        if audio_file_path.is_file():
            print(f"Processando arquivo: {audio_file_path}")
            process_audio_file(audio_file_path)
