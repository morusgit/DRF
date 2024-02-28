from django.urls import path
from users import views, apps

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = apps.UsersConfig.name

router = routers.DefaultRouter()
router.register(r'profile', views.UserViewSet, basename='profile')


urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payments'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
