from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index1'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',views.logout_view,name= 'logout'),
    path('login/loginUser/', views.loginUser, name='loginUser'),
    path('test/', views.TestView.as_view(), name='test'),
    path('signup/', views.get_name, name='signup'),
    path('ao/',views.administrativeOfficer.as_view(), name='administrativeOfficer')
]
