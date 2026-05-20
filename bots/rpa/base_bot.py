import pyautogui
import pywinauto
import time
from loguru import logger

class BaseRPABot:
    """Classe base para robôs que interagem com o sistema operacional e aplicativos desktop"""
    
    def __init__(self):
        # Configuração de segurança do PyAutoGUI (para o mouse se você jogar para o canto da tela)
        pyautogui.FAILSAFE = True
        # Pausa padrão após cada comando do PyAutoGUI
        pyautogui.PAUSE = 0.5
        
    def wait(self, seconds: float):
        """Pausa a execução"""
        time.sleep(seconds)
        
    def take_screenshot(self, filepath: str):
        """Tira um print da tela inteira"""
        pyautogui.screenshot(filepath)
        logger.info(f"Screenshot salva em: {filepath}")
