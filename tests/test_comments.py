import pytest
import logging
from utils.validators import Validator

logger = logging.getLogger(__name__)

@pytest.mark.regression
@pytest.mark.positive
def test_get_comments_for_post(api_client):
    """Тест: получение комментариев для поста"""
    post_id = 1
    response = api_client.get(f'/posts/{post_id}/comments')
    
    Validator.validate_status_code(response, 200)
    
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        first_comment = data[0]
        Validator.validate_field(first_comment, 'postId', post_id)
        Validator.validate_field(first_comment, 'id')
        Validator.validate_field(first_comment, 'name')
        Validator.validate_field(first_comment, 'email')
        Validator.validate_field(first_comment, 'body')
    
    logger.info(f"✅ Получено {len(data)} комментариев для поста #{post_id}")

@pytest.mark.regression
@pytest.mark.positive
def test_create_comment(api_client, data_generator):
    """Тест: создание комментария"""
    comment_data = data_generator.generate_comment(post_id=1)
    response = api_client.post('/comments', json=comment_data)
    
    Validator.validate_status_code(response, 201)
    
    data = response.json()
    Validator.validate_field(data, 'id')
    Validator.validate_field(data, 'postId', comment_data['postId'])
    Validator.validate_field(data, 'name', comment_data['name'])
    
    logger.info(f"✅ Комментарий создан с ID: {data['id']}")