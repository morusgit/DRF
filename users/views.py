from django.db.models.functions import datetime
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserRegistrationSerializer
from users.services import create_product, create_price


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response({'message': 'User registered successfully', 'user_data': serializer.data})

    def perform_create(self, serializer):
        user = serializer.save()
        # Здесь добавьте код для вывода информации о пользователе в консоль
        print(f"New user registered: {user.email}, {user.phone}, {user.city}, {user.avatar}")
        return user


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(APIView):
    def post(self, request, format=None):
        # Получаем данные о платеже из запроса
        user = request.user
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')

        # Создаем продукт в Stripe
        product_id = create_product("Course Subscription", "Subscription to course")

        # Создаем цену в Stripe
        price_id = create_price(product_id, amount, 'RUB')

        # Установка текущей даты и времени для поля payment_date
        payment_date = timezone.now()

        # Создаем запись о платеже в нашей системе
        payment = Payment.objects.create(user=user, amount=amount, payment_method=payment_method,
                                          product_id=product_id, price_id=price_id, payment_date=payment_date)

        # Создаем сессию для платежа в Stripe
        success_url = "http://example.com/success"  # Замените на ваш URL успешного платежа
        cancel_url = "http://example.com/cancel"  # Замените на ваш URL отмены платежа
        session_url = payment.create_checkout_session(success_url, cancel_url)

        if session_url:
            # Если сессия создана успешно, возвращаем URL для оплаты
            return Response({'session_url': session_url}, status=status.HTTP_201_CREATED)
        else:
            # Если возникла ошибка при создании сессии, возвращаем соответствующий ответ
            return Response({'error': 'Failed to create checkout session'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusAPIView(APIView):
    def get(self, request, pk, format=None):
        # Получаем запись о платеже по его идентификатору
        payment = Payment.objects.get(pk=pk)

        # Получаем данные о статусе платежа из Stripe
        # В этом месте мы можем добавить логику для проверки статуса платежа в Stripe

        # Возвращаем данные о статусе платежа в ответе
        return Response({'status': 'Payment status goes here'}, status=status.HTTP_200_OK)
