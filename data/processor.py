import pandas as pd
import os
from datetime import datetime
from loguru import logger

class DataProcessor:
    """Classe responsável pelo tratamento e exportação de dados usando pandas"""
    
    def __init__(self, output_dir="data/exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def clean_prices(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpa as colunas de preços, removendo R$ e convertendo para float"""
        try:
            if 'price' in df.columns:
                # Caso o preço venha como 'R$ 80,00' do scraping
                df['price'] = df['price'].astype(str).str.replace('R$', '').str.replace(',', '.').str.strip()
                df['price'] = pd.to_numeric(df['price'], errors='coerce')
            return df
        except Exception as e:
            logger.error(f"Erro ao limpar preços: {e}")
            return df
            
    def export_to_csv(self, data: list, filename_prefix: str = "PetCompare_export") -> str:
        """Exporta uma lista de dicionários para um arquivo CSV"""
        if not data:
            logger.warning("Nenhum dado para exportar.")
            return ""
            
        df = pd.DataFrame(data)
        df = self.clean_prices(df)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.csv")
        
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Dados exportados para CSV com sucesso: {filename}")
        
        return filename
        
    def export_to_excel(self, data: list, filename_prefix: str = "PetCompare_export") -> str:
        """Exporta uma lista de dicionários para um arquivo Excel (.xlsx)"""
        if not data:
            logger.warning("Nenhum dado para exportar.")
            return ""
            
        df = pd.DataFrame(data)
        df = self.clean_prices(df)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.xlsx")
        
        df.to_excel(filename, index=False, engine='openpyxl')
        logger.info(f"Dados exportados para Excel com sucesso: {filename}")
        
        return filename
