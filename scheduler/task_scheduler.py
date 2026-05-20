from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
import os

class BotScheduler:
    """Gerenciador de agendamentos para rodar os robôs periodicamente"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    def start(self):
        """Inicia o agendador em background"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Agendador de tarefas (APScheduler) iniciado com sucesso.")
            
    def stop(self):
        """Para o agendador"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Agendador de tarefas parado.")
            
    def schedule_daily_scraping(self, func, hour: int = 3, minute: int = 0):
        """
        Agenda uma função de scraping para rodar todos os dias num horário específico.
        Ideal rodar de madrugada (ex: 03:00) para não sobrecarregar.
        """
        trigger = CronTrigger(hour=hour, minute=minute)
        job_id = f"daily_scrape_{func.__name__}"
        
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            name=f"Daily scraping job: {func.__name__}",
            replace_existing=True
        )
        logger.info(f"Tarefa {job_id} agendada para todos os dias às {hour:02d}:{minute:02d}")

# Instância global para ser importada na API
bot_scheduler = BotScheduler()
