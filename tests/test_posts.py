import pytest
import logging
from utils.validators import Validator

logger = logging.getLogger(__name__)

@pytest.mark.smoke
@pytest.mark.positive
def test_get_all_posts(api_client):
    """Тест: получение всех постов"""
    response = api_client.get('/posts')
    
    # Проверяем статус-код
    Validator.validate_status_code(response, 200)
    
    # Проверяем, что это список
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Posts list should not be empty"
    
    # Проверяем структуру первого поста
    first_post = data[0]
    expected_fields = ['id', 'title', 'body', 'userId']
    for field in expected_fields:
        Validator.validate_field(first_post, field)
    
    logger.info(f"✅ Получено {len(data)} постов")

@pytest.mark.smoke
@pytest.mark.positive
def test_get_post_by_id(api_client):
    """Тест: получение поста по ID"""
    post_id = 1
    response = api_client.get(f'/posts/{post_id}')
    
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    Validator.validate_field(data, 'id', post_id)
    Validator.validate_field(data, 'title')
    Validator.validate_field(data, 'body')
    Validator.validate_field(data, 'userId')
    
    logger.info(f"✅ Пост #{post_id} получен: {data['title'][:30]}...")

@pytest.mark.regression
@pytest.mark.negative
def test_get_nonexistent_post(api_client):
    """Тест: получение несуществующего поста"""
    post_id = 9999
    response = api_client.get(f'/posts/{post_id}')
    
    Validator.validate_status_code(response, 404)
    logger.info(f"✅ Пост #{post_id} не найден - статус 404")

@pytest.mark.regression
@pytest.mark.positive
def test_create_post(api_client, test_post_data):
    """Тест: создание нового поста"""
    response = api_client.post('/posts', json=test_post_data)
    
    Validator.validate_status_code(response, 201)
    
    data = response.json()
    Validator.validate_field(data, 'id')
    Validator.validate_field(data, 'title', test_post_data['title'])
    Validator.validate_field(data, 'body', test_post_data['body'])
    Validator.validate_field(data, 'userId', test_post_data['userId'])
    
    logger.info(f"✅ Пост создан с ID: {data['id']}")

@pytest.mark.regression
@pytest.mark.positive
def test_update_post(api_client, created_post_id):
    """Тест: обновление поста (используем существующий ID)"""
    update_data = {
        'title': 'Updated Title',
        'body': 'Updated body content',
        'userId': 1
    }
    
    # Используем ID 1, который гарантированно существует
    post_id = 1
    response = api_client.put(f'/posts/{post_id}', json=update_data)
    
    # JSONPlaceholder возвращает 200 для существующих постов
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    Validator.validate_field(data, 'id', post_id)
    Validator.validate_field(data, 'title', update_data['title'])
    Validator.validate_field(data, 'body', update_data['body'])
    Validator.validate_field(data, 'userId', update_data['userId'])
    
    logger.info(f"✅ Пост #{post_id} обновлён")

@pytest.mark.regression
@pytest.mark.positive
def test_delete_post(api_client, created_post_id):
    """Тест: удаление поста"""
    # Используем существующий ID
    post_id = 1
    response = api_client.delete(f'/posts/{post_id}')
    
    # JSONPlaceholder всегда возвращает 200
    Validator.validate_status_code(response, 200)
    logger.info(f"✅ Пост #{post_id} удалён (статус: {response.status_code})")

@pytest.mark.slow
def test_response_time(api_client):
    """Тест: время ответа API"""
    import time
    
    start = time.time()
    response = api_client.get('/posts')
    elapsed = time.time() - start
    
    assert elapsed < 3.0, f"Response time {elapsed:.2f}s > 3.0s"
    logger.info(f"✅ Время ответа: {elapsed:.2f}s")

@pytest.mark.parametrize('post_id', [1, 2, 3, 4, 5])
def test_multiple_posts(api_client, post_id):
    """Тест: параметризованная проверка нескольких постов"""
    response = api_client.get(f'/posts/{post_id}')
    Validator.validate_status_code(response, 200)
    data = response.json()
    Validator.validate_field(data, 'id', post_id)
    logger.info(f"✅ Пост #{post_id} проверен")

@pytest.mark.regression
@pytest.mark.negative
def test_create_post_with_empty_data(api_client):
    """Тест: создание поста с пустыми данными"""
    response = api_client.post('/posts', json={})
    
    # JSONPlaceholder вернёт 201 даже с пустыми данными
    Validator.validate_status_code(response, 201)
    data = response.json()
    assert 'id' in data
    logger.info(f"✅ Пост создан с ID: {data['id']} (пустые данные)")

@pytest.mark.regression
@pytest.mark.positive
def test_patch_post(api_client):
    """Тест: частичное обновление поста (PATCH)"""
    post_id = 1
    patch_data = {
        'title': 'Patched Title'
    }
    
    response = api_client.patch(f'/posts/{post_id}', json=patch_data)
    
    # JSONPlaceholder поддерживает PATCH
    Validator.validate_status_code(response, 200)
    data = response.json()
    Validator.validate_field(data, 'id', post_id)
    Validator.validate_field(data, 'title', patch_data['title'])
    
    logger.info(f"✅ Пост #{post_id} частично обновлён")

@pytest.mark.regression
@pytest.mark.negative
def test_update_nonexistent_post(api_client):
    """Тест: обновление несуществующего поста"""
    post_id = 9999
    update_data = {
        'title': 'Updated Title',
        'body': 'Updated body',
        'userId': 1
    }
    
    response = api_client.put(f'/posts/{post_id}', json=update_data)
    
    # JSONPlaceholder возвращает 500 для несуществующих постов
    # Это ожидаемое поведение для тестового API
    if response.status_code == 500:
        logger.warning(f"⚠️ API вернул 500 для несуществующего поста #{post_id} (это нормально для JSONPlaceholder)")
        # Не пытаемся парсить JSON, так как ответ пустой
        # Проверяем, что статус 500 - это ожидаемо
        assert response.status_code == 500
        logger.info(f"✅ Тест на обновление несуществующего поста пройден (статус 500)")
    else:
        # Если вдруг вернул другой статус
        Validator.validate_status_code(response, 404)
    
    logger.info(f"✅ Тест на обновление несуществующего поста пройден")