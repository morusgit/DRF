from django.core.management.base import BaseCommand
from users.models import Payment, User
from datetime import datetime
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample payment objects'

    def handle(self, *args, **kwargs):
        # Создаем пользователей, курсы и уроки (если они еще не созданы)
        user1, created = User.objects.get_or_create(email='mail@test.com')
        user2, created = User.objects.get_or_create(email='test@test.com')

        # Создаем платежи
        payment1 = Payment.objects.create(
            user=user1,
            payment_date=datetime.now(),
            amount=Decimal('50.00'),
            payment_method='cash'
        )

        payment2 = Payment.objects.create(
            user=user2,
            payment_date=datetime.now(),
            amount=Decimal('30.00'),
            payment_method='transfer'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created payment objects'))
