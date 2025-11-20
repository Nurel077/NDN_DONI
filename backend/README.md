# NDN Store - Django Backend

Бэкенд для игрового магазина NDN Store на Django с MySQL базой данных.

## Возможности

- ✅ Регистрация и аутентификация пользователей
- ✅ Управление сессиями
- ✅ Профили пользователей со статистикой
- ✅ Настройки пользователей (язык, тема, уведомления)
- ✅ Управление играми
- ✅ Отслеживание игровых сессий
- ✅ Django Admin панель
- ✅ REST API для фронтенда
- ✅ CORS поддержка

## Требования

- Python 3.8+
- MySQL 5.7+ или MariaDB 10.3+
- pip

## Установка

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

**Примечание для Windows:** Если возникают проблемы с установкой `mysqlclient`, используйте:
- Скачайте wheel файл с https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
- Установите: `pip install mysqlclient‑2.2.0‑cp39‑cp39‑win_amd64.whl` (замените версию на свою)

Или используйте альтернативу:
```bash
pip install pymysql
```

Затем в `backend/ndnstore/__init__.py` добавьте:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 2. Настройте MySQL базу данных

Создайте базу данных в MySQL:

```sql
CREATE DATABASE ndnstore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Настройте settings.py

Откройте `backend/ndnstore/settings.py` и обновите настройки базы данных:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ndnstore_db',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 4. Примените миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создайте суперпользователя для админки

```bash
python manage.py createsuperuser
```

### 6. Загрузите начальные данные (опционально)

Создайте игры в админке или через команду:

```bash
python manage.py shell
```

```python
from api.models import Game

games = [
    {'name': 'Space Adventure', 'game_type': 'space', 'game_url': 'https://yandex.ru/games/app/209729', 'icon': 'fas fa-rocket'},
    {'name': 'Война рыцарей', 'game_type': 'medieval', 'game_url': 'https://yandex.ru/games/app/389452', 'icon': 'fas fa-sword'},
    {'name': 'Racing Pro', 'game_type': 'racing', 'game_url': 'https://yandex.ru/games/app/449371', 'icon': 'fas fa-car'},
    {'name': 'Blast Three', 'game_type': 'blast', 'game_url': 'https://nurel077.github.io/NDN_games/', 'icon': 'fas fa-bomb'},
]

for game_data in games:
    Game.objects.create(**game_data)
```

### 7. Запустите сервер

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000`

## API Endpoints

Все API endpoints находятся по адресу `/api/`:

### Аутентификация
- `POST /api/register/` - Регистрация нового пользователя
- `POST /api/login/` - Вход пользователя
- `POST /api/logout/` - Выход пользователя
- `GET /api/validate-session/?session_token=...` - Проверка валидности сессии

### Профиль
- `GET /api/profile/?session_token=...` - Получить профиль пользователя

### Настройки
- `PUT /api/settings/` - Обновить настройки пользователя

### Управление аккаунтом
- `POST /api/change-password/` - Изменить пароль
- `POST /api/change-username/` - Изменить имя пользователя
- `POST /api/delete-account/` - Удалить аккаунт

### Игры
- `GET /api/games/` - Получить список игр
- `POST /api/start-game/` - Начать сессию игры

## Примеры запросов

### Регистрация
```json
POST /api/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!",
    "confirm_password": "Test123!"
}
```

### Вход
```json
POST /api/login/
{
    "email": "test@example.com",
    "password": "Test123!",
    "remember_me": false
}
```

### Получить профиль
```
GET /api/profile/?session_token=ваш_токен
```

### Обновить настройки
```json
PUT /api/settings/
{
    "session_token": "ваш_токен",
    "language": "ru",
    "theme": "dark",
    "email_notifications": true
}
```

## Django Admin

Админ панель доступна по адресу: `http://127.0.0.1:8000/admin/`

Войдите используя учетные данные суперпользователя, созданного на шаге 5.

## Структура проекта

```
backend/
├── api/                    # Приложение API
│   ├── models.py          # Модели базы данных
│   ├── views.py           # API views
│   ├── serializers.py    # Сериализаторы
│   ├── urls.py           # URL маршруты API
│   └── admin.py          # Настройки админки
├── ndnstore/              # Основной проект
│   ├── settings.py       # Настройки Django
│   └── urls.py           # Главные URL маршруты
├── manage.py
├── requirements.txt
└── README.md
```

## Модели базы данных

- **User** (стандартная Django модель) - Пользователи
- **UserProfile** - Расширенный профиль пользователя
- **UserSession** - Сессии пользователей
- **UserSettings** - Настройки пользователей
- **Game** - Игры в магазине
- **GameSession** - Сессии игр пользователей

## Интеграция с фронтендом

Для интеграции с существующим фронтендом (`mega.js`), замените вызовы к `localStorage` на API запросы:

1. Замените `tempStorage.addUser()` на `POST /api/register/`
2. Замените `tempStorage.findUserByEmail()` на `POST /api/login/`
3. Используйте `session_token` из ответа API для последующих запросов
4. Сохраняйте `session_token` в `localStorage` вместо полных данных пользователя

## Разработка

Для разработки рекомендуется использовать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Лицензия

Проект создан для NDN Store.

