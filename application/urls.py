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
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.TestView.as_view(), name='test'),

    # -------------------------------------------------------------------------------------------
    #               TEACHER URLS
    # -------------------------------------------------------------------------------------------
    url(r'^teacher/course/(?P<course_id>[0-9]+)/$',
        login_required(views.TeacherCourseDetailView.as_view(), login_url='application:login'),
        name='teacherCourseViewWithcourse_id'),
    path('teacher/', login_required(views.TeacherView.as_view(), login_url='application:login'), name='teacher'),
    path('teacher/course/<int:course_id>/addtopic', views.content_form, name='contentForm'),
    path('teacher/appointments/', views.AppointmentView.as_view(), name='appointment'),  # NOT USED! Don't Touch!
    path('teacher/appointments/<int:teacherID>', views.appointment_form, name='appointmentWithID'),
    url(r'^teacher/course/(?P<course_id>[0-9]+)/addPerformanceGrade/$', views.grade_form, name='gradeForm'),
    path('teacher/course/<int:course_id>/addAssignment', views.assignment_form, name='assignmentForm'),
    url(r'^teacher/course/(?P<course_id>[0-9]+)/absence/$', views.absence_form, name='absenceForm'),
    url(r'^teacher/course/(?P<course_id>[0-9]+)/behavior/$', views.behavior_form, name='behaviorForm'),
    path('teacher/coordinatedClass', views.TeacherClassCoordinated.as_view(), name='TeacherCoordinator'),
    url(r'^teacher/coordinatedClass/studentCourses/(?P<studentID>[0-9]+)/$',
        login_required(views.PutFinalGrade.as_view(), login_url='application:login'),
        name='putFinalGrade'),
    # -------------------------------------------------------------------------------------------
    #               PARENT URLS
    # -------------------------------------------------------------------------------------------
    path('parent/', views.parentView, name='parent'),
    url(r'^parent/(?P<studentID>[0-9]+)/$', views.parentView, name='parentWithID'),
    url(r'^parent/grades/(?P<studentID>[0-9]+)/$',
        login_required(views.ParentGradeView.as_view(), login_url='application:login'), name='parentGradeWithID'),
    path('parent/grades/', login_required(views.ParentGradeView.as_view(), login_url='application:login'),
         name='parentGrade'),
    path('chooseChild/', login_required(views.ChooseChild.as_view(), login_url='application:login'),
         name='chooseChild'),
    path('parent/attendance', login_required(views.ParentAttendanceView.as_view(), login_url='application:login'),
         name='parentAttendance'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/$',
        login_required(views.CourseView.as_view(), login_url='application:login'), name='courseView'),
    # NOT HANDLED URL PLEASE DONT USE
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<course_id>[0-9]+)/$',
        login_required(views.CourseDetailView.as_view(), login_url='application:login'), name='courseViewWithcourse_id'),
    path('change-password/', views.change_password, name='change_password'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<course_id>[0-9]+)/assignments/$',
        login_required(views.AssignmentView.as_view(), login_url='application:login'), name='assignments'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<course_id>[0-9]+)/materials/$',
        login_required(views.MaterialView.as_view(), login_url='application:login'), name='materials'),
    url(r'^parent/(?P<studentID>[0-9]+)/course/(?P<course_id>[0-9]+)/attendance/$',
        login_required(views.ParentAttendanceView.as_view(), login_url='application:login'), name='parentAttendance'),
    path('parent/<int:studentID>/announcement/', views.AnnouncementView.as_view(), name='announcement'),
    path('parent/<int:studentID>/course/<int:course_id>/notes/', views.NotesView.as_view(), name='CourseNote'),
    path('parent/<int:studentID>/finalResult/', views.FinalGradeView.as_view(), name='finalResult'),

    # -------------------------------------------------------------------------------------------
    #               ADMINISTRATIVE OFFICER URLS
    # -------------------------------------------------------------------------------------------
    path('signup/', views.enroll_student, name='signup'),  # student signup
    path('ao/', login_required(views.AdministrativeOfficer.as_view(), login_url='application:login'), name='ao'),
    url(r'^ao/class/(?P<name>[0-9][A-Z]+)/$', views.timetable_form, name='timetableForm'),
    path('communicationAO/', views.communication_ao, name='communicationAO'),
    path('teacherMasterData/', views.GetTeacherMasterData.as_view(), name='teacherMasterData'),
    path('parentsignup/', views.parent_signup, name='parentSignup'),
    path('composeClass/', views.class_compose, name='classCompose'),
    path('teacheredit/<pk>/', views.EditTeacherMasterData.as_view(), name='teacher-edit'),
    path('teacherMasterData/<pk>', views.GetTeacherMasterData.as_view(), name='teacherMasterData'),
    path('teacheradd/', views.teacher_create, name='teacher-add'),
    url(r'teacher/(?P<pk>[0 -9]+)/delete/$', views.DeleteTeacherMasterData.as_view(), name='teacher-delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
