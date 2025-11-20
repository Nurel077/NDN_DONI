# Пример конфигурации базы данных
# Скопируйте эти настройки в settings.py и укажите свои данные

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ndnstore_db',           # Имя базы данных
        'USER': 'root',                  # Пользователь MySQL
        'PASSWORD': '',                  # Пароль MySQL
        'HOST': 'localhost',             # Хост MySQL
        'PORT': '3306',                  # Порт MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Для Windows, если mysqlclient не устанавливается:
# Используйте pymysql вместо mysqlclient
# 1. pip install pymysql
# 2. В ndnstore/__init__.py добавьте:
#    import pymysql
#    pymysql.install_as_MySQLdb()

