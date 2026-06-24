import markdown
import re
from bs4 import BeautifulSoup
import os

class MarkdownParser:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MarkdownParser, cls).__new__(cls)
        return cls._instance

    def __init__(self, markdown_path='assets/apresentacao.md'):
        self.markdown_path = os.path.join(os.path.dirname(__file__), '..', '..', markdown_path)
        if not hasattr(self, 'initialized'): # Evita re-inicialização
            self.initialized = True

    def get_slides_as_html(self):
        """Lê o arquivo .md, divide em slides e converte cada um para HTML."""
        with open(self.markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        md_slides = re.split(r'\n---\n', content)
        html_slides = [markdown.markdown(slide) for slide in md_slides]
        return html_slides
    
    def get_slides_as_markdown(self):
        """Lê o arquivo .md e divide em uma lista de slides em markdown."""
        with open(self.markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return re.split(r'\n---\n', content)

    def extract_title_and_content(self, md_slide):
        """Extrai o título (h1) e o resto do conteúdo de um slide."""
        lines = md_slide.strip().split('\n')
        title = ""
        content_lines = []
        if lines and lines[0].startswith('# '):
            title = lines[0][2:].strip()
            content_lines = lines[1:]
        else:
            content_lines = lines
        
        content = '\n'.join(content_lines).strip()
        return title, content

parser_singleton = MarkdownParser()
