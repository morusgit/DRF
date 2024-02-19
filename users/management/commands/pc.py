from django.core.management import BaseCommand
import datetime

from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        payment1 = Payment.objects.create(
            date_of_payment=datetime.datetime.now().date(),
            amount=10000,
            payment_type='cash',
            payed_course=Course.objects.get(pk=2),
        )

        payment2 = Payment.objects.create(
            date_of_payment=datetime.datetime.now().date(),
            amount=150000,
            payment_type='cash',
            payed_lesson=Lesson.objects.get(pk=1),
        )

        payment1.save()
        payment2.save()
