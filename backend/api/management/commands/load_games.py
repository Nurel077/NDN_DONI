from django.core.management.base import BaseCommand
from api.models import Game


class Command(BaseCommand):
    help = 'Загрузить начальные игры в базу данных'

    def handle(self, *args, **options):
        games_data = [
            {
                'name': 'Space Adventure',
                'description': 'Космические приключения',
                'game_type': 'space',
                'game_url': 'https://yandex.ru/games/app/209729',
                'icon': 'fas fa-rocket',
                'is_active': True
            },
            {
                'name': 'Война рыцарей',
                'description': 'Средневековые приключения',
                'game_type': 'medieval',
                'game_url': 'https://yandex.ru/games/app/389452',
                'icon': 'fas fa-sword',
                'is_active': True
            },
            {
                'name': 'Racing Pro',
                'description': 'Гонки на выживание',
                'game_type': 'racing',
                'game_url': 'https://yandex.ru/games/app/449371',
                'icon': 'fas fa-car',
                'is_active': True
            },
            {
                'name': 'Blast Three',
                'description': 'Взрывная головоломка',
                'game_type': 'blast',
                'game_url': 'https://nurel077.github.io/NDN_games/',
                'icon': 'fas fa-bomb',
                'is_active': True
            },
        ]

        created_count = 0
        updated_count = 0

        for game_data in games_data:
            game, created = Game.objects.update_or_create(
                game_type=game_data['game_type'],
                defaults=game_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создана игра: {game.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Обновлена игра: {game.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Создано: {created_count}, Обновлено: {updated_count}'
            )
        )

