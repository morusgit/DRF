from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import CoursesConfig
from .views import (LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView,
                    LessonUpdateAPIView, LessonDestroyAPIView, CoursesViewSet, SubscriptionAPIView)

app_name = CoursesConfig.name

# Создаем маршрутизатор
router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='courses')

urlpatterns = [
    # URL-маршруты для курсов


    # URL-маршруты для уроков
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
] + router.urls


