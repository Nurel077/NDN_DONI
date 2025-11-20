# Структура проекта

```
backend/
├── api/                          # Приложение API
│   ├── __init__.py
│   ├── admin.py                 # Настройки Django Admin
│   ├── apps.py
│   ├── models.py                # Модели базы данных
│   ├── serializers.py           # Сериализаторы для REST API
│   ├── urls.py                  # URL маршруты API
│   ├── views.py                 # API views (endpoints)
│   ├── tests.py
│   └── management/
│       └── commands/
│           └── load_games.py     # Команда для загрузки игр
│
├── ndnstore/                    # Основной проект Django
│   ├── __init__.py              # Поддержка pymysql
│   ├── settings.py              # Настройки Django
│   ├── settings.example.py      # Пример настроек БД
│   ├── urls.py                  # Главные URL маршруты
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py                    # Django management script
├── requirements.txt             # Зависимости (Linux/Mac)
├── requirements-windows.txt     # Зависимости (Windows)
├── .gitignore                   # Git ignore файл
├── README.md                    # Полная документация
├── QUICKSTART.md                # Быстрый старт
└── PROJECT_STRUCTURE.md          # Этот файл
```

## Модели базы данных

### User (стандартная Django модель)
- Пользователи системы
- Поля: username, email, password, date_joined

### UserProfile
- Расширенный профиль пользователя
- Поля: user, games_played, last_login_time, created_at, is_active

### UserSession
- Сессии пользователей для аутентификации
- Поля: user, session_token, created_at, expires_at, is_active, remember_me

### UserSettings
- Настройки пользователя
- Поля: user, language, theme, email_notifications, game_notifications, news_notifications

### Game
- Игры в магазине
- Поля: name, description, game_type, game_url, icon, is_active

### GameSession
- Сессии игр пользователей
- Поля: user, game, started_at, ended_at, duration_seconds

## API Endpoints

Все endpoints находятся по адресу `/api/`:

### Аутентификация
- `POST /api/register/` - Регистрация
- `POST /api/login/` - Вход
- `POST /api/logout/` - Выход
- `GET /api/validate-session/` - Проверка сессии

### Профиль и настройки
- `GET /api/profile/` - Получить профиль
- `PUT /api/settings/` - Обновить настройки

### Управление аккаунтом
- `POST /api/change-password/` - Изменить пароль
- `POST /api/change-username/` - Изменить имя
- `POST /api/delete-account/` - Удалить аккаунт

### Игры
- `GET /api/games/` - Список игр
- `POST /api/start-game/` - Начать игру

## Админка

Доступна по адресу `/admin/` после создания суперпользователя.

В админке можно управлять:
- Пользователями и их профилями
- Сессиями пользователей
- Настройками пользователей
- Играми
- Игровыми сессиями

