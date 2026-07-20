import pytest
import logging
from utils.validators import Validator

logger = logging.getLogger(__name__)

@pytest.mark.contract
def test_post_schema_validation(api_client):
    """Контрактный тест: проверка структуры поста"""
    response = api_client.get('/posts/1')
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    
    # Проверяем типы полей
    assert isinstance(data['id'], int), "id должен быть числом"
    assert isinstance(data['userId'], int), "userId должен быть числом"
    assert isinstance(data['title'], str), "title должен быть строкой"
    assert isinstance(data['body'], str), "body должен быть строкой"
    
    # Проверяем, что поля не пустые
    assert data['id'] > 0, "id должен быть больше 0"
    assert data['title'], "title не должен быть пустым"
    assert data['body'], "body не должен быть пустым"
    
    logger.info("✅ Схема поста валидна")

@pytest.mark.contract
def test_user_schema_validation(api_client):
    """Контрактный тест: проверка структуры пользователя"""
    response = api_client.get('/users/1')
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    
    # Проверяем основные поля
    required_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
    for field in required_fields:
        Validator.validate_field(data, field)
    
    # Проверяем вложенную структуру address
    address = data['address']
    address_fields = ['street', 'suite', 'city', 'zipcode', 'geo']
    for field in address_fields:
        Validator.validate_field(address, field)
    
    # Проверяем вложенную структуру company
    company = data['company']
    company_fields = ['name', 'catchPhrase', 'bs']
    for field in company_fields:
        Validator.validate_field(company, field)
    
    logger.info("✅ Схема пользователя валидна")

@pytest.mark.contract
def test_comment_schema_validation(api_client):
    """Контрактный тест: проверка структуры комментария"""
    response = api_client.get('/comments/1')
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    
    # Проверяем поля
    required_fields = ['id', 'postId', 'name', 'email', 'body']
    for field in required_fields:
        Validator.validate_field(data, field)
    
    # Проверяем типы
    assert isinstance(data['id'], int)
    assert isinstance(data['postId'], int)
    assert isinstance(data['name'], str)
    assert isinstance(data['email'], str)
    assert isinstance(data['body'], str)
    
    logger.info("✅ Схема комментария валидна")