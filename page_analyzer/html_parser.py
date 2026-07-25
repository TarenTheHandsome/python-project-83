import requests
from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self, url):
        self.url = url
        self.response = None
        self.resp = None
        self.soup = None
        self.error = None
        try:
            self.response = requests.get()
            self.response.raise_for_status()  # Проверяем статус ответа
            self.resp = self.response.content
            self.soup = BeautifulSoup(self.resp, 'lxml')
        except Exception:
            self.error = 'Error'

    def get_h1(self):
        if self.error or not self.soup:
            return ''
        header = self.soup.h1
        header_text = header.get_text(strip=True) if header else ''
        return header_text

    def get_title(self):
        if self.error or not self.soup:
            return ''
        title = self.soup.title
        title_text = title.get_text(strip=True) if title else ''
        return title_text

    def get_description(self):
        if self.error or not self.soup:
            return ''
        meta = self.soup.find('meta', {'name': 'description'})
        description = meta.get('content', '') if meta else ''
        return description
