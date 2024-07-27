import requests
from pathlib import Path
import webbrowser
from common_paths import TRANSCRIPTION_OUTPUT_PATH

apiKey = "6UlOOoY/kkmprunma/qNDg"

str_personas = TRANSCRIPTION_OUTPUT_PATH / 'input' / 'personas.txt'
str_contexto = TRANSCRIPTION_OUTPUT_PATH / 'input' / 'contexto.txt'

url = "https://gpt-templates.saiapplications.com"
headers = {"X-Api-Key": apiKey}

txt_files = list(TRANSCRIPTION_OUTPUT_PATH.glob('*.txt'))

css_styles = """
<style>
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}

h1, h2, h3 {
    color: #FF8C00;
}

li, strong, p {
    color: #008000;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

h2 {
    font-size: 20px;
    margin-top: 20px;
    margin-bottom: 10px;
}

ul {
    list-style-type: disc;
    margin-left: 40px;
}

li {
    margin-bottom: 10px;
}

p {
    line-height: 1.6;
}
</style>
"""

if not txt_files:
    print(f"Não foram encontrados arquivos .txt no diretório {TRANSCRIPTION_OUTPUT_PATH}.")
else:
    for txt_file in txt_files:
        if txt_file.is_file():
            print(f"Lendo o arquivo: {txt_file.name}")
            with open(txt_file, 'r', encoding='utf-8') as file:
                str_reuniao = file.read()

            print(f"Enviando o conteúdo do arquivo {txt_file.name} para a API...")
            data = {
                "inputs": {
                    "str_reuniao": str_reuniao,
                    "str_personas": str_personas.read_text(encoding='utf-8'),
                    "str_contexto": str_contexto.read_text(encoding='utf-8'),
                }
            }

            response = requests.post(f"{url}/api/templates/668de04202493d3063a9d7fa/execute", json=data, headers=headers)
            if response.status_code == 200:
                print(f"Resultado para o arquivo {txt_file.name} recebido.")
                html_content = response.text
                print(response.text)

                # Incluir o CSS no conteúdo HTML
                html_with_css = f"<html><head>{css_styles}</head><body>{html_content}</body></html>"

                # Salvar o conteúdo HTML em um arquivo
                output_file = TRANSCRIPTION_OUTPUT_PATH / f"{txt_file.stem}_output.html"
                with open(output_file, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_with_css)

                # Abrir o arquivo HTML no navegador
                webbrowser.open(f"file://{output_file.resolve()}")
            else:
                print(f"Erro ao processar o arquivo {txt_file.name}: {response.status_code}")
