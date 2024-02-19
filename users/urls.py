from django.urls import path

from users import views, apps

app_name = apps.UsersConfig.name


urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payments'),
]
