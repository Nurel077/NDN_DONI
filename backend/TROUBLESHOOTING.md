# Решение проблем

## Проблема: Сайт не открывается

### 1. Проверьте, запущен ли сервер

```bash
python manage.py runserver
```

Должно появиться сообщение:
```
Starting development server at http://127.0.0.1:8000/
```

### 2. Проверьте настройки базы данных

Проект настроен на SQLite по умолчанию (не требует MySQL).

Если хотите использовать MySQL:
- Установите: `pip install pymysql`
- Файл `ndnstore/__init__.py` уже настроен автоматически

### 3. Примените миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Проверьте ошибки

```bash
python manage.py check
```

Должно быть: `System check identified no issues (0 silenced).`

## Проблема: ModuleNotFoundError

### MySQLdb не найден

**Решение 1 (рекомендуется):** Используйте SQLite (уже настроено)

**Решение 2:** Установите pymysql:
```bash
pip install pymysql
```

Файл `ndnstore/__init__.py` автоматически использует pymysql.

## Проблема: Ошибки при регистрации/входе

### Проверьте, что профиль создается

Сигналы настроены автоматически. Если проблемы:
1. Убедитесь, что `api.apps.ApiConfig` в INSTALLED_APPS
2. Перезапустите сервер

## Проблема: CORS ошибки

Настройки CORS уже включены в `settings.py`:
- `CORS_ALLOW_ALL_ORIGINS = True` (для разработки)

Если проблемы:
1. Проверьте, что `corsheaders` в INSTALLED_APPS
2. Проверьте, что `CorsMiddleware` в MIDDLEWARE

## Проблема: 404 ошибки

### API не работает

Проверьте URL:
- Главная: http://127.0.0.1:8000/
- API игры: http://127.0.0.1:8000/api/games/
- Админка: http://127.0.0.1:8000/admin/

### Проверьте urls.py

Убедитесь, что в `ndnstore/urls.py` есть:
```python
path('api/', include('api.urls')),
```

## Проблема: Админка не работает

1. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

2. Войдите по адресу: http://127.0.0.1:8000/admin/

## Проблема: База данных пустая

### Загрузите игры

```bash
python manage.py load_games
```

Или добавьте через админку.

## Общие команды для диагностики

```bash
# Проверка проекта
python manage.py check

# Проверка миграций
python manage.py showmigrations

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver

# Загрузка игр
python manage.py load_games
```

## Логи и отладка

Если сервер не запускается, проверьте:
1. Нет ли ошибок в терминале
2. Не занят ли порт 8000
3. Установлены ли все зависимости: `pip install -r requirements.txt`

## Контакты для помощи

Если проблема не решена:
1. Проверьте логи Django в терминале
2. Убедитесь, что все зависимости установлены
3. Проверьте версию Python (должна быть 3.8+)

