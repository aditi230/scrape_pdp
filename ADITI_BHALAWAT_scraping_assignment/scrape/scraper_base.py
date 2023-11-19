import requests
from bs4 import BeautifulSoup

class ScraperBase:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.soup = None

    def scrape(self):
        response = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.content, 'html.parser')