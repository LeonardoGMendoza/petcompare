import pyautogui
from loguru import logger
from bots.rpa.base_bot import BaseRPABot

class MouseKeyboardBot(BaseRPABot):
    """Robô focado em automação de cliques, digitação e busca por imagens na tela"""
    
    def click_image(self, image_path: str, confidence: float = 0.8, clicks: int = 1) -> bool:
        """Localiza uma imagem na tela e clica nela"""
        logger.info(f"Procurando imagem: {image_path}")
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                pyautogui.click(location.x, location.y, clicks=clicks)
                logger.info(f"Clique realizado em ({location.x}, {location.y})")
                return True
            else:
                logger.warning(f"Imagem não encontrada: {image_path}")
                return False
        except Exception as e:
            logger.error(f"Erro ao buscar imagem: {e}")
            return False
            
    def type_text(self, text: str, interval: float = 0.05):
        """Digita um texto simulando um humano"""
        logger.info(f"Digitando texto (oculto no log por segurança)...")
        pyautogui.write(text, interval=interval)
        
    def press_key(self, key_name: str):
        """Pressiona uma tecla específica (ex: 'enter', 'tab', 'esc')"""
        logger.info(f"Pressionando tecla: {key_name}")
        pyautogui.press(key_name)
        
    def scroll(self, amount: int):
        """Rola a tela (positivo para cima, negativo para baixo)"""
        pyautogui.scroll(amount)
