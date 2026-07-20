import pytest
import logging
from clients.api_client import APIClient
from models.data_generators import TestDataGenerator
from utils.logger import setup_logger

# Настраиваем логирование
setup_logger()
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def api_client():
    """Фикстура для API-клиента"""
    return APIClient()

@pytest.fixture(scope='session')
def data_generator():
    """Фикстура для генерации данных"""
    return TestDataGenerator()

@pytest.fixture
def test_post_data(data_generator):
    """Фикстура с тестовыми данными для поста"""
    return data_generator.generate_post()

@pytest.fixture
def created_post_id(api_client):
    """Создаёт существующий пост для тестов (используем ID из API)"""
    # Вместо создания нового поста, используем существующий ID
    # JSONPlaceholder не сохраняет созданные посты, поэтому используем существующий
    existing_post_id = 1  # Это существующий пост в JSONPlaceholder
    logger.info(f"✅ Используем существующий пост с ID: {existing_post_id}")
    return existing_post_id

@pytest.fixture
def created_post_data(api_client, data_generator):
    """Создаёт пост и возвращает данные"""
    post_data = data_generator.generate_post()
    response = api_client.post('/posts', json=post_data)
    assert response.status_code == 201
    post_id = response.json()['id']
    logger.info(f"✅ Создан тестовый пост с ID: {post_id}")
    return {'id': post_id, 'data': post_data}