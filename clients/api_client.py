import logging
import requests
import time
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import settings

logger = logging.getLogger(__name__)

class APIClient:
    """Базовый HTTP-клиент с retry-механизмом"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(settings.DEFAULT_HEADERS)
        
        # Настройка retry только для сетевых ошибок и специфических статусов
        retry_strategy = Retry(
            total=settings.RETRY_COUNT,
            backoff_factor=settings.RETRY_DELAY,
            status_forcelist=settings.RETRY_STATUSES,  # без 500
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"],
            raise_on_status=False  # Не поднимать исключение при статусах из forcelist
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def _log_request(self, method: str, url: str, **kwargs):
        """Логирование запроса"""
        logger.info(f"🔵 {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"📦 Request body: {kwargs['json']}")
        if 'params' in kwargs:
            logger.debug(f"🔍 Query params: {kwargs['params']}")
            
    def _log_response(self, response: requests.Response):
        """Логирование ответа"""
        logger.info(f"🟢 {response.status_code} {response.url}")
        if response.text:
            logger.debug(f"📦 Response: {response.text[:200]}...")
        
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Базовый метод для выполнения запросов с retry"""
        url = f"{self.base_url}{endpoint}"
        
        # Настройка таймаутов
        if 'timeout' not in kwargs:
            kwargs['timeout'] = (settings.CONNECTION_TIMEOUT, settings.READ_TIMEOUT)
        
        # Логируем запрос
        self._log_request(method, url, **kwargs)
        
        # Выполняем запрос с повторными попытками
        try:
            start_time = time.time()
            response = self.session.request(method, url, **kwargs)
            elapsed_time = time.time() - start_time
            
            # Логируем ответ
            self._log_response(response)
            logger.info(f"⏱️ Время выполнения: {elapsed_time:.2f}s")
            
            return response
            
        except requests.exceptions.Timeout as e:
            logger.error(f"❌ Таймаут при запросе к {url}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Ошибка при запросе к {url}: {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET-запрос"""
        return self._request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST-запрос"""
        return self._request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT-запрос"""
        return self._request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE-запрос"""
        return self._request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """PATCH-запрос"""
        return self._request('PATCH', endpoint, **kwargs)