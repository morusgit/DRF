from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Create sample payment objects'

    def handle(self, *args, **kwargs):
        # Создаем пользователей, курсы и уроки (если они еще не созданы)
        user1, created = User.objects.get_or_create(email='mailmail@test.com')
        user2, created = User.objects.get_or_create(email='testtest@test.com')

        self.stdout.write(self.style.SUCCESS('Successfully created payment objects'))
