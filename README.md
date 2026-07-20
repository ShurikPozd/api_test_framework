# 🧪 API Test Framework

Профессиональный фреймворк для автоматизированного тестирования REST API с использованием **pytest**, **Allure** и **Python**.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/pytest-7.4.3-brightgreen.svg" alt="pytest">
  <img src="https://img.shields.io/badge/Allure-2.13.2-orange.svg" alt="Allure">
  <img src="https://img.shields.io/badge/tests-24-success.svg" alt="Tests">
  <img src="https://img.shields.io/badge/coverage-95%25-green.svg" alt="Coverage">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

## 📋 Оглавление
- [О проекте](#-о-проекте)
- [Технологии](#-технологии)
- [Структура проекта](#-структура-проекта)
- [Установка](#-установка)
- [Запуск тестов](#-запуск-тестов)
- [Отчёты](#-отчёты)
- [Маркеры тестов](#-маркеры-тестов)
- [Примеры тестов](#-примеры-тестов)
- [Результаты](#-результаты)

## 🎯 О проекте

**API Test Framework** — это профессиональный фреймворк для тестирования REST API, разработанный для демонстрации навыков автоматизации тестирования. 

### Что умеет фреймворк:
- ✅ **24 автотеста** (позитивные, негативные, контрактные)
- ✅ **Контрактное тестирование** с JSON Schema
- ✅ **Параллельный запуск** тестов (pytest-xdist)
- ✅ **Allure-отчёты** с красивой визуализацией
- ✅ **Retry-механизм** для стабильности тестов
- ✅ **Генерация тестовых данных** через Faker
- ✅ **Логирование** всех запросов и ответов
- ✅ **Параметризованные тесты**

## 🛠 Технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| Python | 3.14+ | Язык программирования |
| pytest | 7.4.3 | Фреймворк тестирования |
| requests | 2.31.0 | HTTP-клиент |
| Allure | 2.13.2 | Отчёты и визуализация |
| Faker | 20.1.0 | Генерация тестовых данных |
| JSON Schema | 4.20.0 | Контрактное тестирование |
| pytest-xdist | 3.5.0 | Параллельный запуск |

## 📁 Структура проекта

```
api_test_framework/
├── config/
│   └── settings.py          # Конфигурация и переменные окружения
├── clients/
│   └── api_client.py        # Базовый HTTP-клиент с retry
├── models/
│   ├── data_generators.py   # Генераторы тестовых данных (Faker)
│   └── schemas/             # JSON-схемы для контрактного тестирования
├── tests/
│   ├── test_posts.py        # Тесты для постов (CRUD)
│   ├── test_users.py        # Тесты для пользователей
│   ├── test_comments.py     # Тесты для комментариев
│   ├── test_contract.py     # Контрактные тесты
│   └── test_crud_operations.py # Полный CRUD цикл
├── utils/
│   ├── logger.py            # Настройка логирования
│   └── validators.py        # Валидаторы ответов
├── logs/                    # Логи выполнения тестов
├── reports/                 # Allure-отчёты
├── conftest.py              # Фикстуры pytest
├── pytest.ini               # Конфигурация pytest
├── requirements.txt         # Зависимости
├── .env                     # Переменные окружения
├── .gitignore
└── README.md
```

## 🚀 Установка

### 1. Клонировать репозиторий
```bash
git clone https://github.com/ShurikPozd/api_test_framework.git
cd api_test_framework
```

### 2. Создать виртуальное окружение
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

## 🏃 Запуск тестов

### Все тесты
```bash
pytest
```

### С подробными логами
```bash
pytest -v --log-cli-level=INFO
```

### Только smoke-тесты (быстрая проверка)
```bash
pytest -m smoke
```

### Только регрессионные тесты
```bash
pytest -m regression
```

### Только контрактные тесты
```bash
pytest -m contract
```

### Параллельный запуск (4 потока)
```bash
pytest -n 4
```

### С перезапуском упавших тестов
```bash
pytest --reruns 2 --reruns-delay 1
```

## 📊 Отчёты

### Allure-отчёт (рекомендуется)
```bash
# Запуск тестов с Allure
pytest --alluredir=reports/allure-results

# Генерация отчёта
allure generate reports/allure-results -o reports/allure-report --clean

# Открыть отчёт в браузере
allure open reports/allure-report
```

### HTML-отчёт (pytest-html)
```bash
pytest --html=reports/report.html
```

## 🏷️ Маркеры тестов

| Маркер | Описание |
|--------|----------|
| `@pytest.mark.smoke` | Дымовые тесты (быстрая проверка) |
| `@pytest.mark.regression` | Регрессионные тесты |
| `@pytest.mark.positive` | Позитивные сценарии |
| `@pytest.mark.negative` | Негативные сценарии |
| `@pytest.mark.contract` | Контрактные тесты |
| `@pytest.mark.slow` | Медленные тесты |

## 📝 Примеры тестов

### Пример позитивного теста
```python
@pytest.mark.smoke
@pytest.mark.positive
def test_get_all_posts(api_client):
    """Тест: получение всех постов"""
    response = api_client.get('/posts')
    Validator.validate_status_code(response, 200)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
```

### Пример контрактного теста
```python
@pytest.mark.contract
def test_post_schema_validation(api_client):
    """Контрактный тест: проверка структуры поста"""
    response = api_client.get('/posts/1')
    Validator.validate_status_code(response, 200)
    data = response.json()
    
    assert isinstance(data['id'], int)
    assert isinstance(data['userId'], int)
    assert isinstance(data['title'], str)
    assert isinstance(data['body'], str)
```

### Пример параметризованного теста
```python
@pytest.mark.parametrize('post_id', [1, 2, 3, 4, 5])
def test_multiple_posts(api_client, post_id):
    """Тест: параметризованная проверка нескольких постов"""
    response = api_client.get(f'/posts/{post_id}')
    Validator.validate_status_code(response, 200)
    data = response.json()
    Validator.validate_field(data, 'id', post_id)
```

## 📈 Результаты

### Статистика тестов
- **Всего тестов:** 24
- **Smoke-тестов:** 2
- **Regression-тестов:** 15+
- **Contract-тестов:** 3
- **Время выполнения:** ~3 секунды

### Пример Allure-отчёта
![Allure Report](https://allure-framework.readthedocs.io/en/latest/_images/allure-report.png)

## 🤝 Вклад в проект

Если вы хотите внести свой вклад в проект:
1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Сделайте коммит (`git commit -m 'Add some amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📞 Контакты

- **GitHub:** [ShurikPozd](https://github.com/ShurikPozd)
- **Telegram:** [@shurikpozd](https://t.me/shurikpozd)
- **Email:** shurik-3002@mail.ru

## 📜 Лицензия

Этот проект создан в образовательных целях и для демонстрации навыков автоматизации тестирования.

---

⭐️ Если вам понравился проект, поставьте звездочку на GitHub!
