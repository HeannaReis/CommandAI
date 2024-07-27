import requests

def buscar_noticias_pais(pais, api_key):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': pais,  # Código do país
        'apiKey': api_key  # Substitua pelo seu API Key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao acessar a API para o país {pais}: {response.status_code}")

def buscar_noticias_varios_paises(paises, api_key):
    noticias_combinadas = []
    for pais in paises:
        try:
            noticias = buscar_noticias_pais(pais, api_key)
            noticias_combinadas.extend(noticias['articles'])
        except Exception as e:
            print(f"Erro ao buscar notícias para o país {pais}: {e}")
    return noticias_combinadas

# Exemplo de uso
api_key = 'baa0b83953234c5a8d5777157f0b33df'  # Substitua pelo seu API Key
paises = ['us', 'gb', 'br']  # Códigos dos países: Estados Unidos (us), Reino Unido (gb), Brasil (br)
noticias = buscar_noticias_varios_paises(paises, api_key)

for artigo in noticias:
    print(f"{artigo['title']}")
