from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


from courses.models import Course, Lesson


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='плательщик')
    payment_date = models.DateField(auto_now=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')])

    def __str__(self):
        # pylint: disable=no-member
        return f"Payment by {self.user.email} for {self.course or self.lesson} on {self.payment_date}"
