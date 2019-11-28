from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect  # , render_to_response
from django.urls import reverse
import csv, io
from django.db.models import Q

from .models import StudentCourse, PerformanceGrade, Parent, Content, Course, Student, ClassInfo, TeacherCourse, \
    ParentStudent, Attendance, Assignment
from django.views import generic
from application.forms import StudentForm, ParentSignUpForm, ClassComposeForm, ContentForm, PerformanceGradeForm, \
    AbsenceForm, AssignmentForm


# Create your views here.

# -----------------------------------------------------------------------------------------------
####### ADMINISTRATIVE OFFICER AREA##########
# -----------------------------------------------------------------------------------------------
class AdministrativeOfficer(generic.ListView):
    template_name = 'administrativeOfficer/base.html'

    def get_queryset(self):
        return "salam"


@login_required(login_url='application:login')
def enrollStudent(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            messages.success(request, 'Student has been successfully added')
            return render(request, 'administrativeOfficer/enrollStudent.html', {'form': StudentForm()})

            # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'administrativeOfficer/enrollStudent.html', {'form': form})


@login_required(login_url='application:login')
def classCompose(request):
    if request.method == 'POST':
        form = ClassComposeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            classInfo = form.save()
            classInfo.refresh_from_db()

            if Student.objects.filter(classID=None).count() < classInfo.totalStudentsNumber:
                for student in Student.objects.filter(classID=None):
                    student.classID = classInfo
                    student.save()
            else:
                i = 0
                for student in Student.objects.filter(classID=None):
                    if i < classInfo.totalStudentsNumber:
                        i += 1
                        student.classID = classInfo
                        student.save()

            messages.success(request, 'Class has been successfully added')

            return render(request, 'administrativeOfficer/classCompose.html',
                          {'form': form, 'numberOfSeats': numberOfSeats(), 'numberOfStudents': numberOfStudents()})
    else:
        form = ClassComposeForm()

    return render(request, 'administrativeOfficer/classCompose.html',
                  {'form': form, 'numberOfSeats': numberOfSeats(), 'numberOfStudents': numberOfStudents()})


def numberOfSeats():
    number = ClassInfo.objects.aggregate((Sum('totalStudentsNumber')))['totalStudentsNumber__sum']
    return number


def numberOfStudents():
    number = Student.objects.filter(classID=None).count()
    print(number)
    return number


@login_required(login_url='application:login')
def parentSignup(request):
    if request.method == 'POST':
        form = ParentSignUpForm(request.POST)
        try:
            user = User.objects.get(username=request.POST['username'], )
            return render(request, 'administrativeOfficer/parentSignup.html',
                          {'error_message': 'Username Exist...Try Something Else !', 'form': ParentSignUpForm()})
        except User.DoesNotExist:
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                parent = Parent.objects.create(user=user, )
                for student in form.cleaned_data.get('studentID'):
                    ParentStudent.objects.create(studentID=student, parentID=parent)

                messages.success(request, 'Parent has been successfully added')

                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password2']
                sendmailtoparent(username, email, password)  # send credentials to a parent

                return render(request, 'administrativeOfficer/parentSignup.html', {'form': ParentSignUpForm()})
            else:
                return render(request, 'administrativeOfficer/parentSignup.html',
                              {'error_message': 'Invalid Information', 'form': ParentSignUpForm()})
    else:
        form = ParentSignUpForm()
    return render(request, 'administrativeOfficer/parentSignup.html', {'form': form})


def sendmailtoparent(username, email, password):
    send_mail('School Account Credentials',
              'Dear Sir/Madam,\n We hope that this email finds you in a good health.\n' +
              'This is your credentials for accessing the school website\n' +
              'Username: ' + username + '\nPassword: ' + password + '\n' +
              'you can access our website by pressing this link: http://127.0.0.1:8000/application/login/' + '\n' +
              'Have a nice day.',
              'admofficer658@gmail.com',
              [email],
              fail_silently=False)


def communicationWithParent(request):
    return render(request, 'administrativeOfficer/communication.html')


# -----------------------------------------------------------------------------------------------
####### PARENT AREA##########
# -----------------------------------------------------------------------------------------------

class TestView(generic.ListView):
    template_name = 'parent/afterloginparent.html'

    def get_queryset(self):
        return "salam"


class CourseView(generic.ListView):
    template_name = 'parent/course.html'
    context_object_name = 'studentID'

    def get_queryset(self):
        return self.kwargs['studentID']


class CourseDetailView(generic.ListView):
    template_name = 'parent/course.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Content.objects.filter(courseID=self.kwargs['courseID'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['courseID'])
        context['courseID'] = self.kwargs['courseID']
        return context


class MaterialView(generic.ListView):
    template_name = 'parent/material.html'
    context_object_name = 'courseID'

    def get_queryset(self):
        return self.kwargs['courseID']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MaterialView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        if Assignment.objects.filter(courseID=self.kwargs['courseID']):
            context['assignments'] = Assignment.objects.filter(courseID=self.kwargs['courseID'])
        # if Course.objects.get(ID=self.kwargs['courseID']).assignment:
        # context['assignments'] = Course.objects.get(ID=self.kwargs['courseID']).assignment.url
        # context['assignmentName'] = Course.objects.get(ID=self.kwargs['courseID']).assignment.name
        else:
            context['assignments'] = []
        return context


class ParentView(generic.ListView):
    template_name = 'parent/afterloginparent.html'
    context_object_name = 'allStudentCourses'

    def get_queryset(self):
        return Course.objects.filter(studentcourse__studentID=self.kwargs['studentID'])  # GET STUDENT ID HERE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        context['parentStudent'] = ParentStudent.objects.filter(studentID=self.kwargs['studentID'])
        if ClassInfo.objects.filter(student__ID=self.kwargs['studentID']).exists():
            context['studentClass'] = ClassInfo.objects.get(student__ID=self.kwargs['studentID'])
        return context


class ChooseChild(generic.ListView):
    template_name = 'parent/chooseChild.html'
    context_object_name = 'allChildren'

    def get_queryset(self):
        return ParentStudent.objects.filter(parentID=self.request.user.parent.ID)  # GET STUDENT ID HERE


class ParentAttendanceView(generic.ListView):
    template_name = 'parent/attendancep.html'
    context_object_name = 'studentID'

    def get_queryset(self):
        return self.kwargs['studentID']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentAttendanceView, self).get_context_data(**kwargs)
        context['courseID'] = self.kwargs['courseID']
        context['attendances'] = Attendance.objects.filter(Q(studentCourseID__studentID=self.kwargs['studentID']),
                                                           Q(studentCourseID__courseID=self.kwargs[
                                                               'courseID']), ).order_by('date')
        # create new Vew for handling attendance divided into months, need to add new constraint to the query,
        # and send Month_Name into next url
        return context


class ParentGradeView(generic.ListView):
    template_name = 'parent/gradep.html'
    context_object_name = 'allGrades'

    def get_queryset(self):
        return PerformanceGrade.objects.filter(studentCourseID__studentID=self.kwargs[
            'studentID'])  # GET STUDENTCOURSEID HERE ; should I send studentID to the url here?

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentGradeView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        context['studentCourse'] = StudentCourse.objects.filter(
            studentID=self.kwargs['studentID'])  # GET STUDENT ID HERE

        columns = 0
        for studentcourse in context['studentCourse']:
            gradeCounter = 0
            for grade in context['allGrades']:
                if grade.studentCourseID.courseID.name == studentcourse.courseID.name:
                    gradeCounter += 1
            if gradeCounter > columns:
                columns = gradeCounter
        context['columns'] = range(columns)
        return context


@login_required(login_url='application:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully.')
            return redirect(reverse('application:change_password'))
        else:
            return render(request, 'parent/change_password.html',
                          {'error_message': 'Invalid Information', 'form': PasswordChangeForm(user=request.user)})
    else:
        return render(request, 'parent/change_password.html', {'form': PasswordChangeForm(user=request.user)})


def Announcement(request):
    return render(request, 'parent/announcement.html')


# -----------------------------------------------------------------------------------------------
####### TEACHER AREA##########
# -----------------------------------------------------------------------------------------------

class TeacherView(generic.ListView):
    template_name = 'teacher/teacherAfterLogin.html'
    context_object_name = 'allTeacherCourses'

    def get_queryset(self):
        return TeacherCourse.objects.filter(teacherID=self.request.user.teacher.ID)


class TeacherCourseDetailView(generic.ListView):
    template_name = 'teacher/course.html'
    context_object_name = 'contents'

    def get_queryset(self):
        return Content.objects.filter(courseID=self.kwargs['courseID'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherCourseDetailView, self).get_context_data(**kwargs)
        context['courseID'] = self.kwargs['courseID']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['courseID'])
        context['assignments'] = Assignment.objects.filter(courseID=self.kwargs['courseID'])
        return context


class AbsenceView(generic.ListView):
    template_name = 'teacher/absence.html'
    context_object_name = 'behaviour'

    def get_queryset(self):
        return Content.objects.filter(courseID=self.kwargs['courseID'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AbsenceView, self).get_context_data(**kwargs)
        context['courseID'] = self.kwargs['courseID']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['courseID'])
        return context


@login_required(login_url='application:login')
def absenceForm(request, courseID):
    if request.method == 'POST':
        form = AbsenceForm(request.POST, courseID=courseID)
        if form.is_valid():
            form.save()
            return redirect('application:teacher')
    else:
        form = AbsenceForm(courseID=courseID)
    return render(request, 'teacher/absence.html', {'form': form, 'courseID': courseID, })


@login_required(login_url='application:login')
def contentForm(request, courseID):
    if request.method == 'POST':
        form = ContentForm(request.POST, user=request.user)
        if form.is_valid():
            unsavedForm = form.save(commit=False)
            unsavedForm.courseID = Course.objects.get(ID=courseID)
            unsavedForm.save()
            return redirect('application:teacher')
    else:
        form = ContentForm(user=request.user)
    return render(request, 'teacher/addTopicORMaterial.html', {'form': form, 'courseID': courseID, })


@login_required(login_url='application:login')
def gradeForm(request, courseID):
    if request.method == 'POST':
        form = PerformanceGradeForm(request.POST, courseID=courseID)
        if form.is_valid():
            form.save()
            return redirect('application:teacher')
    else:
        form = PerformanceGradeForm(courseID=courseID)
    return render(request, 'teacher/grade.html', {'form': form, 'courseID': courseID, })


@login_required(login_url='application:login')
def assignmentForm(request, courseID):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            unsavedForm = form.save(commit=False)
            unsavedForm.courseID = Course.objects.get(ID=courseID)
            unsavedForm.save()
            return redirect('application:teacher')
    else:
        form = AssignmentForm()
    return render(request, 'teacher/addAssignment.html', {'form': form, 'courseID': courseID, })


# -----------------------------------------------------------------------------------------------
####### GENERAL AREA##########
# -----------------------------------------------------------------------------------------------

class IndexView(generic.ListView):
    template_name = 'application/index.html'

    def get_queryset(self):
        return "salam"


class LoginView(generic.ListView):
    template_name = 'application/login.html'

    def get_queryset(self):
        return "salam"


@login_required(login_url='application:login')
def logout_view(request):
    logout(request)
    return redirect('application:index')


def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    teacher = user.teacher
                    return redirect('application:teacher')
                except:
                    try:
                        parent = user.parent
                        numberOfStudent = ParentStudent.objects.filter(parentID=parent.ID).count()

                        if parent.lastLogin is False:
                            parent.lastLogin = True
                            parent.save()
                            return redirect('application:change_password')
                        else:
                            if (numberOfStudent == 1):
                                studentID = ParentStudent.objects.get(parentID=parent.ID).studentID.ID
                                return redirect('application:parentWithID', studentID)
                            else:
                                return redirect('application:chooseChild')
                        # return render(request,'parent/afterloginparent.html', {'studentID': studentID, 'studentCourses': studentCourses})
                    except:
                        try:
                            administrativeOfficer = user.administrativeofficer
                            return redirect('application:administrativeOfficer')
                        except:
                            try:
                                principle = user.principle
                                return HttpResponse("<h1>you are logged in as principle</h1>")
                            except:
                                return HttpResponse("<h1>you are a hacker</h1>")
        else:
            return render(request, 'application/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'application/login.html')

####### PRINCIPLE AREA##########
