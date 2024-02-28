from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


class CourseLessonSubscriptionAPITest(TestCase):
    def setUp(self):
        """
        Устанавливаем начальные данные для тестов.
        """
        # Создаем клиента API
        self.client = APIClient()

        # Удаляем все уроки перед созданием новых
        Lesson.objects.all().delete()

        # Создаем пользователей
        self.user_moderator = User.objects.create(email='moderator@example.com', password='testpassword')
        self.user_owner = User.objects.create(email='owner@example.com', password='testpassword')
        self.user_not_moderator = User.objects.create(email='notmoderator@example.com', password='testpassword')

        # Создаем курс
        self.course = Course.objects.create(title='Test Course 1', description='Test description 1', owner=self.user_owner)

        # Создаем уроки
        self.lesson1 = Lesson.objects.create(title='Lesson 1', description='Lesson description 1', course=self.course, owner=self.user_owner)
        self.lesson2 = Lesson.objects.create(title='Lesson 2', description='Lesson description 2', course=self.course, owner=self.user_owner)

    def test_crud_lessons(self):
        """
        Проверка CRUD операций с уроками.
        """
        # Авторизуем пользователя с правами владельца курса
        self.client.force_authenticate(user=self.user_owner)

        # Создание нового урока с указанием существующего курса
        response = self.client.post('/lessons/create/', {'title': 'New Lesson', 'description': 'New Lesson description',
                                                         'course': self.course})
        # Проверка успешного создания урока
        self.assertEqual(response.status_code, 201,
                         f"Expected status code 201, but got {response.status_code}. Response data: {response.data}")

        # Получение списка уроков
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что созданный урок есть в списке
        lesson_title = 'New Lesson'
        lessons = response.data['results']
        lesson_exists = any(lesson['title'] == lesson_title for lesson in lessons)
        self.assertTrue(lesson_exists, f"Lesson '{lesson_title}' not found in the list of lessons")

        # Получаем id созданного урока
        lesson_id = response.data['results'][0]['id']

        # Обновление урока
        response = self.client.put(f'/lessons/{lesson_id}/update/',
                                   {'title': 'Updated Lesson', 'description': 'Updated description',
                                    'course': self.course})
        # Проверка успешного обновления урока
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Lesson')

        # Удаление урока
        response = self.client.delete(f'/lessons/{lesson_id}/delete/')
        # Проверка успешного удаления урока
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=lesson_id).exists())

    def test_subscription(self):
        """
        Проверка функционала подписки на курс.
        """
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user_not_moderator)

        # Подписываемся на курс
        response = self.client.post('/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Проверяем, что подписка существует
        self.assertTrue(Subscription.objects.filter(user=self.user_not_moderator, course=self.course).exists())

        # Повторная подписка на тот же курс должна удалить подписку
        response = self.client.post('/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user_not_moderator, course=self.course).exists())

        # Проверяем, что невозможно создать подписку без указания ID курса
        response = self.client.post('/subscribe/', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'ID курса не указан')
