from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Course, Lesson, Subscription
from .validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'owner']
        validators = [
            YouTubeLinkValidator(field='video_link')
        ]


class SimpleLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link']
        validators = [
            YouTubeLinkValidator(field='video_link')
        ]


class CourseSerializer(serializers.ModelSerializer):
    num_of_lessons = serializers.SerializerMethodField()
    lessons = SimpleLessonSerializer(many=True, read_only=True)
    # Добавляем поле для указания подписки пользователя на курс
    is_subscribed = serializers.SerializerMethodField()

    def get_num_of_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'num_of_lessons', 'lessons', 'owner', 'is_subscribed']

    def get_is_subscribed(self, obj):
        # Получаем текущего пользователя
        user = self.context['request'].user
        # Проверяем, подписан ли пользователь на данный курс
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

# В этом сериализаторе мы добавили поле is_subscribed, которое будет указывать,
# подписан ли текущий пользователь на данный курс.
# Метод get_is_subscribed проверяет, подписан ли пользователь на курс, и возвращает соответствующее значение.


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course']