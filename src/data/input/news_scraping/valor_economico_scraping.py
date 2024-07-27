import requests
from bs4 import BeautifulSoup

def extrair_noticias_valor():
    url = 'https://valor.globo.com/ultimas-noticias/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar os elementos das notícias
        noticias = soup.find_all('div', class_='feed-post')
        
        lista_noticias = []
        for noticia in noticias:
            titulo = noticia.find('a', class_='feed-post-link').get_text(strip=True)
            link = noticia.find('a', class_='feed-post-link')['href']
            lista_noticias.append({'titulo': titulo, 'link': link})
        
        return lista_noticias
    else:
        raise Exception(f"Erro ao acessar a página: {response.status_code}")

# Chamar a função e imprimir as notícias extraídas
noticias = extrair_noticias_valor()
for noticia in noticias:
    print(f"Título: {noticia['titulo']}")
    print(f"Link: {noticia['link']}")
    print()
