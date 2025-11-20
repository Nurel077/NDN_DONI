from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создать суперпользователя с кастомными данными'

    def handle(self, *args, **options):
        username = 'Xx__xX'
        password = '12345'
        email = 'admin@ndnstore.com'
        
        # Проверяем, существует ли пользователь
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.email = email
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Пользователь {username} обновлен как суперпользователь')
            )
        else:
            # Создаем нового пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Суперпользователь {username} создан успешно!')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nЛогин: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Пароль: {password}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'\nВойдите в админку: http://127.0.0.1:8000/admin/')
        )

