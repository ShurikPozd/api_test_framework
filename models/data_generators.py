from faker import Faker
import random

fake = Faker()

class TestDataGenerator:
    """Генератор тестовых данных"""
    
    @staticmethod
    def generate_post(user_id: int = None):
        """Генерация данных для поста"""
        return {
            'title': fake.sentence(nb_words=5),
            'body': fake.paragraph(nb_sentences=3),
            'userId': user_id or random.randint(1, 10)
        }
    
    @staticmethod
    def generate_user():
        """Генерация данных для пользователя"""
        return {
            'name': fake.name(),
            'username': fake.user_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'website': fake.url()
        }
    
    @staticmethod
    def generate_comment(post_id: int = None):
        """Генерация данных для комментария"""
        return {
            'name': fake.sentence(nb_words=3),
            'email': fake.email(),
            'body': fake.paragraph(nb_sentences=2),
            'postId': post_id or random.randint(1, 100)
        }