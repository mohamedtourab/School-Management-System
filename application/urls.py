from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('index/login/', views.LoginView.as_view(), name='login'),
    path('index/login/login_user',views.loginUser, name='loginUser')
]
