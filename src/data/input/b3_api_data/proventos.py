import requests
from bs4 import BeautifulSoup

def obter_proventos_petr4(simbolo):
    url = f'https://www.fundamentus.com.br/proventos.php?papel={simbolo}'
    
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
        raise Exception(f"Erro ao acessar a página: {response.status_code}")

def extrair_proventos(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Encontrar a tabela de proventos
    tabela = soup.find('table', {'id': 'resultado'})
    
    if tabela is None:
        raise Exception("Tabela de proventos não encontrada")
    
    # Extraindo os dados da tabela de proventos
    dados = []
    cabecalho = [th.text.strip() for th in tabela.find('thead').find_all('th')]
    for tr in tabela.find('tbody').find_all('tr'):
        linha = [td.text.strip() for td in tr.find_all('td')]
        dados.append(linha)
    
    return cabecalho, dados

def analisar_dividendos(dados):
    print(f"{'Data':<12} {'Valor':<10} {'Tpo':<15} {'Data Pagamento':<8} {'Por quantas ações (%)':<18}")

    for linha in dados:
        data, provento, valor, tipo, rendimento = linha
        print(f"{data:<12} {provento:<10} {valor:<15} {tipo:<8} {rendimento:<18}")

def main():
    simbolo = 'PETR4'
    html = obter_proventos_petr4(simbolo)
    cabecalho, dados = extrair_proventos(html)
    
    # Mostrar o cabeçalho da tabela
    print("Cabeçalho da Tabela:")
    print(cabecalho)
    
    # Mostrar os dados dos proventos
    print("\nDados dos Proventos:")
    analisar_dividendos(dados)

if __name__ == "__main__":
    main()
