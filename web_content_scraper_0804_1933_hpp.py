# 代码生成时间: 2025-08-04 19:33:16
import quart
from quart import jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Any, Dict

# Constants
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}

# Error messages
ERROR_INVALID_URL = "Invalid URL provided."
ERROR_URL_NOT_REACHABLE = "Unable to reach the URL."
ERROR_PARSING_FAILED = "Failed to parse the content of the page."

class WebContentScraper:
    """A class to handle web content scraping."""

    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()

    def fetch_content(self) -> str:
        """Fetches the HTML content of the provided URL."""
        try:
            response = self.session.get(self.url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            # Handle exceptions related to network issues
            raise Exception(ERROR_URL_NOT_REACHABLE) from e

    def parse_content(self, content: str) -> BeautifulSoup:
        """Parses the HTML content using BeautifulSoup."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            return soup
        except Exception as e:
            # Handle exceptions related to parsing issues
            raise Exception(ERROR_PARSING_FAILED) from e

    def get_page_title(self, soup: BeautifulSoup) -> str:
        "