import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Базовый URL
    BASE_URL = os.getenv('BASE_URL', 'https://jsonplaceholder.typicode.com')
    
    # Таймауты
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    CONNECTION_TIMEOUT = int(os.getenv('CONNECTION_TIMEOUT', 10))
    READ_TIMEOUT = int(os.getenv('READ_TIMEOUT', 20))
    
    # Заголовки по умолчанию
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Параллельный запуск
    PARALLEL_WORKERS = int(os.getenv('PARALLEL_WORKERS', 4))
    
    # Retry настройки (убираем 500 из status_forcelist)
    RETRY_COUNT = int(os.getenv('RETRY_COUNT', 2))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 1))
    # Оставляем только сетевые ошибки, не 500
    RETRY_STATUSES = [429, 502, 503, 504]  # убрали 500

settings = Settings()