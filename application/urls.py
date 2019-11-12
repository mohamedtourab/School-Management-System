from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/loginUser/', views.loginUser, name='loginUser'),
    path('test/', views.TestView.as_view(), name='test'),
]
