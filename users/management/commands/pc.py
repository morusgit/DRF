from django.core.management import BaseCommand
import datetime

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = 'Create sample payment objects'

    def handle(self, *args, **kwargs):
        # Создаем пользователей, курсы и уроки (если они еще не созданы)
        user1, created = User.objects.get_or_create(email='mail@test.com')
        user2, created = User.objects.get_or_create(email='test@test.com')

        # Создаём платежи
        payment1 = Payment.objects.create(
            payer=user1,
            date_of_payment=datetime.datetime.now().date(),
            amount=77555599,
            payment_type='cash',

        )

        payment2 = Payment.objects.create(
            payer=user2,
            date_of_payment=datetime.datetime.now().date(),
            amount=88777799,
            payment_type='cash',

        )

        self.stdout.write(self.style.SUCCESS('Successfully created payment objects'))
