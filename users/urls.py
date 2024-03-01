from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet, UserRegistrationView, PaymentCreateAPIView

app_name = UsersConfig.name

# Описание маршрутизации для ViewSet
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'payment', PaymentViewSet, basename='payment')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
] + router.urls
