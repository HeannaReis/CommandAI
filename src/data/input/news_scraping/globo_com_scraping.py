import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

def verificar_permissao(user_agent, url):
    rp = RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    permissao = rp.can_fetch(user_agent, url)
    print(f"Permissão de acesso: {permissao}")
    return permissao

def extrair_noticias():
    url = 'https://www.globo.com/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    if not verificar_permissao(user_agent, url):
        raise Exception(f"O User-Agent '{user_agent}' não tem permissão para acessar o site {url} de acordo com o robots.txt")

    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status da resposta HTTP: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias = soup.find_all('a', class_='post__link')
        print(f"Número de notícias encontradas: {len(noticias)}")
        
        lista_noticias = []
        for noticia in noticias:
            titulo = noticia.get_text(strip=True)
            link = noticia['href']
            lista_noticias.append({'titulo': titulo, 'link': link})
        
        return lista_noticias
    else:
        raise Exception(f"Erro ao acessar a API: {response.status_code}")

def formatar_noticias_para_prompt(noticias):
    prompt = "Aqui estão as últimas notícias:\n"
    for noticia in noticias:
        prompt += f"Título: {noticia['titulo']}\nLink: {noticia['link']}\n\n"
    return prompt

def main():
    try:
        noticias = extrair_noticias()
        prompt = formatar_noticias_para_prompt(noticias)
        print(prompt)
        # Aqui você pode integrar o prompt com o modelo de robô assistente
        # Por exemplo, enviar o prompt para uma API de modelo de linguagem
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
