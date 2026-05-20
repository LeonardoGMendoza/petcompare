import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time
import random
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class BaseScraper:
    """Classe base para todos os robôs de scraping"""
    
    def __init__(self, use_selenium=True, headless=True):
        self.use_selenium = use_selenium
        self.headless = os.getenv("SELENIUM_HEADLESS", str(headless)).lower() == "true"
        self.driver = None
        self.session = requests.Session()
        
        # Headers padrão para burlar bloqueios básicos
        self.session.headers.update({
            "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        })

    def start_driver(self):
        """Inicializa o Selenium WebDriver com ChromeDriver"""
        if not self.use_selenium:
            return
            
        logger.info("Iniciando Selenium WebDriver...")
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={self.session.headers['User-Agent']}")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def close_driver(self):
        """Fecha o WebDriver"""
        if self.driver:
            logger.info("Fechando Selenium WebDriver...")
            self.driver.quit()
            self.driver = None

    def random_sleep(self, min_seconds=2, max_seconds=5):
        """Pausa aleatória para simular comportamento humano"""
        time.sleep(random.uniform(min_seconds, max_seconds))
        
    def get_soup(self, url: str) -> BeautifulSoup:
        """Pega o HTML via Requests e retorna um BeautifulSoup"""
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
