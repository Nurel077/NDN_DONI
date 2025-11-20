# Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

**Для Windows (если mysqlclient не устанавливается):**
```bash
pip install pymysql
```

Затем создайте файл `backend/ndnstore/__init__.py` и добавьте:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 2. Создание базы данных MySQL

```sql
CREATE DATABASE ndnstore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 3. Настройка settings.py

Откройте `ndnstore/settings.py` и обновите настройки базы данных:
- `NAME` - имя базы данных (ndnstore_db)
- `USER` - пользователь MySQL
- `PASSWORD` - пароль MySQL

## 4. Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

## 6. Загрузка игр

```bash
python manage.py load_games
```

## 7. Запуск сервера

```bash
python manage.py runserver
```

## Доступ

- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

## Тестирование API

### Регистрация
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!",
    "confirm_password": "Test123!"
  }'
```

### Вход
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "remember_me": false
  }'
```

### Получить игры
```bash
curl http://127.0.0.1:8000/api/games/
```

