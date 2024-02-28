from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsOwner, IsModerator, IsNotModerator
from .models import Course, Lesson, Subscription
from .paginators import MyPagination
from .serializers import CourseSerializer, LessonSerializer


# Представления для курсов

class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator, IsOwner]
    pagination_class = MyPagination

    def perform_create(self, serializer):
        # При создании курса добавляем текущего пользователя как владельца
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModerator, IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsModerator, IsOwner]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator, IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


# Представления для уроков
class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            # Если пользователь является модератором, показываем все уроки
            return Lesson.objects.all()
        elif user.is_authenticated:
            # Если пользователь аутентифицирован, показываем только его уроки
            return Lesson.objects.filter(owner=user)
        else:
            # Если пользователь не аутентифицирован, показываем пустой queryset
            return Lesson.objects.none()

    def get_permissions(self):
        if self.request.method == 'GET':
            # Для GET-запросов проверяем только IsAuthenticated и IsNotModerator
            return [permissions.IsAuthenticated(), IsNotModerator()]
        elif self.request.method == 'POST':
            # Для POST-запросов проверяем только IsAuthenticated и IsModerator
            return [permissions.IsAuthenticated(), IsModerator()]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator or IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated and IsNotModerator]

    def perform_create(self, serializer):
        # При создании урока добавляем текущего пользователя как владельца
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner or IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получаем пользователя из запроса
        user = request.user
        # Получаем id курса из данных запроса
        course_id = request.data.get('course_id')
        # Проверяем, передан ли идентификатор курса в запросе
        if not course_id:
            return Response({"message": "ID курса не указан"}, status=400)
        # Получаем объект курса из базы данных
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли уже подписка у пользователя на этот курс
        subs_item = Subscription.objects.filter(user=user, course=course)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})


# class CourseListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# class CourseRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# class CourseCreateAPIView(generics.CreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# class CourseUpdateAPIView(generics.UpdateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# class CourseDestroyAPIView(generics.DestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer