import requests
from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.resp = self.response.content
        self.soup = BeautifulSoup(self.resp, 'lxml')

    def get_h1(self):
        header = self.soup.h1
        header_text = header.get_text(strip=True) if header else ''
        return header_text

    def get_title(self):
        title = self.soup.title
        title_text = title.get_text(strip=True) if title else ''
        return title_text

    def get_description(self):
        meta = self.soup.find('meta', {'name': 'description'})
        description = meta.get('content', '') if meta else ''
        return description
