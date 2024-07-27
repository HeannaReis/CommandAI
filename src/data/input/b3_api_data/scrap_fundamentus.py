import requests
from bs4 import BeautifulSoup

def obter_dados_fundamentais(simbolo):
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={simbolo}&tipo=2'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Erro ao acessar a API: {response.status_code}")

def extrair_dados_financeiros(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    dados = {}
    
    # Extraindo dados da tabela principal
    tabela_principal = soup.find('table', class_='w728')
    linhas = tabela_principal.find_all('tr')
    
    for linha in linhas:
        colunas = linha.find_all('td')
        if len(colunas) == 4:
            label1 = colunas[0].get_text(strip=True)
            valor1 = colunas[1].get_text(strip=True)
            label2 = colunas[2].get_text(strip=True)
            valor2 = colunas[3].get_text(strip=True)
            dados[label1] = valor1
            dados[label2] = valor2
    
    # Extraindo dados de outras tabelas
    tabelas_adicionais = soup.find_all('table', class_='w728')[1:]
    for tabela in tabelas_adicionais:
        linhas = tabela.find_all('tr')
        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) == 4:
                label1 = colunas[0].get_text(strip=True)
                valor1 = colunas[1].get_text(strip=True)
                label2 = colunas[2].get_text(strip=True)
                valor2 = colunas[3].get_text(strip=True)
                dados[label1] = valor1
                dados[label2] = valor2
    
    return dados

# Exemplo de uso
simbolo = 'PETR4'
html = obter_dados_fundamentais(simbolo)
dados_financeiros = extrair_dados_financeiros(html)

for chave, valor in dados_financeiros.items():
    print(f"{chave}: {valor}")
