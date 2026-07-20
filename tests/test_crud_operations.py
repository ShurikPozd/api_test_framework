import pytest
import logging
from models.data_generators import TestDataGenerator

logger = logging.getLogger(__name__)

@pytest.mark.regression
class TestCRUDOperations:
    """Тесты CRUD операций"""
    
    def test_full_crud_cycle(self, api_client):
        """Полный CRUD цикл: Create -> Read -> Update -> Delete"""
        # 1. CREATE
        create_data = TestDataGenerator.generate_post()
        create_response = api_client.post('/posts', json=create_data)
        assert create_response.status_code == 201
        created_post = create_response.json()
        post_id = created_post['id']
        logger.info(f"✅ Создан пост #{post_id}")
        
        # 2. READ - проверяем, что пост создался (JSONPlaceholder НЕ сохраняет)
        read_response = api_client.get(f'/posts/{post_id}')
        # JSONPlaceholder возвращает 404 для созданных постов (не сохраняет)
        if read_response.status_code == 404:
            logger.warning(f"⚠️ JSONPlaceholder не сохраняет посты (это нормально)")
            # Пропускаем проверку, так как это особенность API
        else:
            assert read_response.status_code == 200
            read_post = read_response.json()
            assert read_post['title'] == create_data['title']
            logger.info(f"✅ Прочитан пост #{post_id}")
        
        # 3. UPDATE - используем существующий пост
        existing_id = 1
        update_data = {
            'title': 'Updated via CRUD test',
            'body': 'Updated body',
            'userId': 1
        }
        update_response = api_client.put(f'/posts/{existing_id}', json=update_data)
        assert update_response.status_code == 200
        logger.info(f"✅ Обновлён пост #{existing_id}")
        
        # 4. DELETE
        delete_response = api_client.delete(f'/posts/{existing_id}')
        assert delete_response.status_code == 200
        logger.info(f"✅ Удалён пост #{existing_id}")
    
    def test_create_and_read(self, api_client, data_generator):
        """Создание и чтение поста"""
        post_data = data_generator.generate_post()
        
        # Create
        create_resp = api_client.post('/posts', json=post_data)
        assert create_resp.status_code == 201
        post_id = create_resp.json()['id']
        
        # Read - проверяем, что пост не сохраняется (особенность JSONPlaceholder)
        read_resp = api_client.get(f'/posts/{post_id}')
        if read_resp.status_code == 404:
            logger.warning(f"⚠️ Созданный пост #{post_id} не сохранён (особенность JSONPlaceholder)")
            # Это ожидаемое поведение для JSONPlaceholder
        else:
            assert read_resp.status_code == 200
            logger.info(f"✅ Пост #{post_id} успешно прочитан")