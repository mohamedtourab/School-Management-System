from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect  # , render_to_response
from django.urls import reverse

from .models import StudentCourse, PerformanceGrade, Parent, Content, Course, Student, ClassInfo
from django.views import generic
from application.forms import StudentForm, ParentSignUpForm, ClassComposeForm


# Create your views here.

class TestView(generic.ListView):
    template_name = 'parent/afterloginparent.html'

    def get_queryset(self):
        return "salam"


class AdministrativeOfficer(generic.ListView):
    template_name = 'administrativeOfficer/base.html'

    def get_queryset(self):
        return "salam"


class CourseView(generic.ListView):
    template_name = 'parent/course.html'

    def get_queryset(self):
        return "salam"


class CourseDetailView(generic.ListView):
    template_name = 'parent/course.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Content.objects.filter(courseID=self.kwargs['courseID'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['courseID'])
        return context


class ParentView(generic.ListView):
    template_name = 'parent/afterloginparent.html'
    context_object_name = 'allStudentCourses'

    def get_queryset(self):
        return StudentCourse.objects.filter(studentID=self.request.user.parent.studentID)  # GET STUDENT ID HERE


class ParentAttendanceView(generic.ListView):
    template_name = 'parent/attendancep.html'

    def get_queryset(self):
        return "salam"


class ParentGradeView(generic.ListView):
    template_name = 'parent/gradep.html'
    context_object_name = 'allGrades'

    def get_queryset(self):
        return PerformanceGrade.objects.filter(
            studentCourseID__studentID=self.request.user.parent.studentID)  # GET STUDENTCOURSEID HERE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentGradeView, self).get_context_data(**kwargs)
        context['studentCourse'] = StudentCourse.objects.filter(
            studentID=self.request.user.parent.studentID)  # GET STUDENT ID HERE

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


class IndexView(generic.ListView):
    template_name = 'application/index.html'

    def get_queryset(self):
        return "salam"


class LoginView(generic.ListView):
    template_name = 'application/login.html'

    def get_queryset(self):
        return "salam"


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
                    return render(request, 'teacher/teacherAfterLogin.html', )
                except:
                    try:
                        parent = user.parent
                        # studentID = parent.studentID
                        # studentCourses = StudentCourse.objects.filter(studentID=studentID)
                        return redirect('application:parent')
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


def classCompose(request):
    if request.method == 'POST':
        form = ClassComposeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            classInfo = form.save()
            classInfo.refresh_from_db()

            print(Student.objects.filter(classID=None))
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
    number = Student.objects.all().count()
    return number


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
                Parent.objects.create(user=user, studentID=form.cleaned_data.get('studentID'))
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
    send_mail('Credentials',
              'Username: ' + username + '\nPassword: ' + password,
              'admofficer658@gmail.com',
              [email],
              fail_silently=False)


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
