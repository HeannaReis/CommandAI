from bs4 import BeautifulSoup

class TextProcessor:
    def extract_values_from_json(self, data):
        if isinstance(data, dict):
            return ' '.join([str(value) for value in data.values()])
        elif isinstance(data, list):
            return ' '.join([self.extract_values_from_json(item) for item in data])
        return str(data)

    def extract_text_from_html(self, html):
        if not html.strip().startswith('<'):
            print("Aviso: A entrada parece um caminho de arquivo, não um conteúdo HTML.")
            return html
        soup = BeautifulSoup(html, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
