from django.core.management.base import BaseCommand
from users.models import User



class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='cs777666@gmail.com',
            first_name='Admin',
            last_name='Admin777',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password('3472')
        user.save()
