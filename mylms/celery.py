from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.utils import timezone

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylms.settings')

# Создание экземпляра объекта Celery
app = Celery('mylms')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Настройка расписания для celery-beat
app.conf.beat_schedule = {
    'block-inactive-users-every-month': {
        'task': 'mylms.tasks.block_inactive_users',
        'schedule': timezone.timedelta(days=1),  # Запускать каждый день
    },
}
