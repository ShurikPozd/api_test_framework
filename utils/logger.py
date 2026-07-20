import logging
import sys
from pathlib import Path
from config.settings import settings

def setup_logger():
    """Настройка логирования"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Создаём папку для логов
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Корневой логгер
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Логи в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(console_handler)
    
    # Логи в файл
    file_handler = logging.FileHandler('logs/api_tests.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(file_handler)
    
    return logger