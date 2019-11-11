from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    # path('login/loginUser/', views.userLogin, name='loginUser'),
]
