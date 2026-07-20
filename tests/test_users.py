import pytest
import logging
from utils.validators import Validator

logger = logging.getLogger(__name__)

@pytest.mark.smoke
@pytest.mark.positive
def test_get_users(api_client):
    """Тест: получение списка пользователей"""
    response = api_client.get('/users')
    
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Проверяем структуру пользователя
    first_user = data[0]
    expected_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
    for field in expected_fields:
        Validator.validate_field(first_user, field)
    
    logger.info(f"✅ Получено {len(data)} пользователей")

@pytest.mark.regression
@pytest.mark.positive
def test_get_user_by_id(api_client):
    """Тест: получение пользователя по ID"""
    user_id = 1
    response = api_client.get(f'/users/{user_id}')
    
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    Validator.validate_field(data, 'id', user_id)
    Validator.validate_field(data, 'name')
    Validator.validate_field(data, 'email')
    
    logger.info(f"✅ Пользователь #{user_id}: {data['name']}")