from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'application'

urlpatterns = [
    # -------------------------------------------------------------------------------------------
    #               GENERAL URLS
    # -------------------------------------------------------------------------------------------
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index1'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.TestView.as_view(), name='test'),

    # -------------------------------------------------------------------------------------------
    #               TEACHER URLS
    # -------------------------------------------------------------------------------------------
    url(r'^teacher/course/(?P<courseID>[0-9]+)/$',
        login_required(views.TeacherCourseDetailView.as_view(), login_url='application:login'),
        name='teacherCourseViewWithCourseId'),
    path('teacher/', login_required(views.TeacherView.as_view(), login_url='application:login'), name='teacher'),
    path('teacher/course/<int:courseID>/addtopic', views.contentForm, name='contentForm'),
    url(r'^teacher/course/(?P<courseID>[0-9]+)/addPerformanceGrade/$', views.gradeForm, name='gradeForm'),
    path('teacher/course/<int:courseID>/addAssignment', views.assignmentForm, name='assignmentForm'),
    url(r'^teacher/course/(?P<courseID>[0-9]+)/behaviour/$', views.absenceForm, name='absenceForm'),

    # -------------------------------------------------------------------------------------------
    #               PARENT URLS
    # -------------------------------------------------------------------------------------------
    path('parent/', login_required(views.ParentView.as_view(), login_url='application:login'), name='parent'),
    url(r'^parent/(?P<studentID>[0-9]+)/$', login_required(views.ParentView.as_view(), login_url='application:login'),
        name='parentWithID'),
    url(r'^parent/grades/(?P<studentID>[0-9]+)/$',
        login_required(views.ParentGradeView.as_view(), login_url='application:login'), name='parentGradeWithID'),
    path('parent/grades/', login_required(views.ParentGradeView.as_view(), login_url='application:login'),
         name='parentGrade'),
    path('parentsignup/', views.parentSignup, name='parentSignup'),
    path('chooseChild/', login_required(views.ChooseChild.as_view(), login_url='application:login'),
         name='chooseChild'),
    path('parent/attendance', login_required(views.ParentAttendanceView.as_view(), login_url='application:login'),
         name='parentAttendance'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/$',
        login_required(views.CourseView.as_view(), login_url='application:login'), name='courseView'),
    # NOT HANDLED URL PLEASE DONT USE
    path('composeClass/', views.classCompose, name='classCompose'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<courseID>[0-9]+)/$',
        login_required(views.CourseDetailView.as_view(), login_url='application:login'), name='courseViewWithCourseId'),
    path('change-password/', views.change_password, name='change_password'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<courseID>[0-9]+)/materials/$',
        login_required(views.MaterialView.as_view(), login_url='application:login'), name='materials'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<courseID>[0-9]+)/attendance/$',
        login_required(views.ParentAttendanceView.as_view(), login_url='application:login'), name='parentAttendance'),
    path('parent/announcement/', views.AnnouncementView.as_view(), name='announcement'),

    # -------------------------------------------------------------------------------------------
    #               ADMINISTRATIVE OFFICER URLS
    # -------------------------------------------------------------------------------------------
    path('signup/', views.enrollStudent, name='signup'),  # student signup
    path('ao/', login_required(views.AdministrativeOfficer.as_view(), login_url='application:login'), name='ao'),
    url(r'^ao/class/(?P<name>[0-9][A-Z]+)/$', views.timetableForm, name='timetableForm'),
    path('communicationAO/', views.communicationAO, name='communicationAO'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
