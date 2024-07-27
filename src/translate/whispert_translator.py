import whisper
import pyaudio
import numpy as np

# Inicializa o modelo Whisper
model = whisper.load_model("base")

# Configurações de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Inicializa o PyAudio
audio = pyaudio.PyAudio()

# Abre o stream de áudio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Diga algo em português...")

try:
    audio_buffer = []

    while True:
        # Lê dados do microfone
        data = stream.read(CHUNK)
        audio_buffer.append(np.frombuffer(data, dtype=np.int16).flatten().astype(np.float32) / 32768.0)

        # Processa o áudio a cada 5 segundos
        if len(audio_buffer) * CHUNK / RATE >= 5:
            audio_data = np.concatenate(audio_buffer)
            audio_buffer = []

            # Transcreve e traduz o áudio usando Whisper
            result = model.transcribe(audio_data, task="translate", language="pt")

            # Exibe a tradução
            print(f"Tradução para o inglês: {result['text']}")

except KeyboardInterrupt:
    print("Interrompido pelo usuário")

    # Fecha o stream de áudio
    stream.stop_stream()
    stream.close()
    audio.terminate()
