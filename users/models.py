from django.contrib.auth.models import AbstractUser
from django.db import models
from users.services import create_checkout_session


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


from courses.models import Course, Lesson


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')])
    # Добавляем поля для связи с продуктом и ценой в Stripe
    product_id = models.CharField(max_length=50, blank=True, null=True)
    price_id = models.CharField(max_length=50, blank=True, null=True)

    def create_checkout_session(self, success_url, cancel_url):
        """Создать сессию для платежа."""
        if not self.product_id or not self.price_id:
            return None
        return create_checkout_session(self.price_id, success_url, cancel_url)

    def __str__(self):
        # pylint: disable=no-member
        return f"Payment by {self.user.email} for {self.course or self.lesson} on {self.payment_date}"
