from django.urls import path, re_path
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index1'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.TestView.as_view(), name='test'),
    path('signup/', views.enrollStudent, name='signup'),  # student signup
    path('ao/', views.AdministrativeOfficer.as_view(), name='administrativeOfficer'),
    path('parent/', views.ParentView.as_view(), name='parent'),
    path('parent/grades/', views.ParentGradeView.as_view(), name='parentGrade'),
    path('parentsignup/', views.parentSignup, name='parentSignup'),
]
