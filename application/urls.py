from django.urls import path, re_path
from django.conf.urls import url
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
    url(r'^parent/(?P<studentID>[0-9]+)/$', views.ParentView.as_view(), name='parentWithID'),
    url(r'^parent/grades/(?P<studentID>[0-9]+)/$', views.ParentGradeView.as_view(), name='parentGradeWithID'),
    path('parent/grades/', views.ParentGradeView.as_view(), name='parentGrade'),
    path('parentsignup/', views.parentSignup, name='parentSignup'),
    path('chooseChild/', views.ChooseChild.as_view(), name='chooseChild'),
    path('parent/attendance', views.ParentAttendanceView.as_view(), name='parentAttendance'),
    path('parent/course/', views.CourseView.as_view(), name='courseView'),  # NOT HANDLED URL PLEASE DONT USE
    path('composeClass/', views.classCompose, name='classCompose'),
    url(r'^parent/course/(?P<courseID>[0-9]+)/$', views.CourseDetailView.as_view(), name='courseViewWithCourseId'),
    path('change-password/', views.change_password, name='change_password'),
    url(r'^teacher/course/(?P<courseID>[0-9]+)/$', views.TeacherCourseDetailView.as_view(),
        name='teacherCourseViewWithCourseId'),
    path('teacher/', views.TeacherView.as_view(), name='teacher'),
    path('teacher/addtopic/', views.contentForm, name='contentForm'),
    url(r'^teacher/course/(?P<courseID>[0-9]+)/addPerformanceGrade/$', views.gradeForm, name='gradeForm'),
]
