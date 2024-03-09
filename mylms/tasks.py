from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import get_user_model
from courses.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)

    # Проверяем, прошло ли более 4 часов с момента последнего обновления
    if timezone.now() - course.updated_at > timedelta(hours=4):
        # Отправляем уведомление
        # Ваш код отправки электронной почты
        send_mail(
            'Course Update Notification',
            'The course you subscribed to has been updated.',
            'from@example.com',
            [Subscription.user.email],
            fail_silently=False,
        )

        # Обновляем время последнего уведомления
        course.updated_at = timezone.now()
        course.save()


@shared_task
def block_inactive_users():
    # Получаем модель пользователя
    User = get_user_model()

    # Определяем период неактивности пользователя (30 дней)
    inactive_period = timezone.now() - timezone.timedelta(days=30)

    # Получаем пользователей, которые не заходили в систему более месяца
    inactive_users = User.objects.filter(last_login__lte=inactive_period)

    # Блокируем неактивных пользователей
    inactive_users.update(is_active=False)
