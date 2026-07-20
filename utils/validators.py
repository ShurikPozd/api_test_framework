import logging
from typing import Dict, Any
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

class Validator:
    """Валидатор ответов API"""
    
    @staticmethod
    def validate_status_code(response, expected_status: int):
        """Проверка статус-кода"""
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}"
        logger.info(f"✅ Status code: {response.status_code}")
    
    @staticmethod
    def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]):
        """Проверка JSON-схемы"""
        try:
            validate(instance=data, schema=schema)
            logger.info("✅ Schema validation passed")
        except ValidationError as e:
            logger.error(f"❌ Schema validation failed: {e}")
            raise
    
    @staticmethod
    def validate_field(data: Dict[str, Any], field: str, expected_value: Any = None):
        """Проверка наличия поля и его значения"""
        assert field in data, f"Field '{field}' not found in response"
        if expected_value is not None:
            assert data[field] == expected_value, \
                f"Field '{field}' expected '{expected_value}', got '{data[field]}'"
        logger.info(f"✅ Field '{field}' validated")