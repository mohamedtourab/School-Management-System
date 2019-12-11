import datetime

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

from .models import StudentCourse, PerformanceGrade, Parent, Content, Course, Student, ClassInfo, TeacherCourse, \
    ParentStudent, Attendance, Assignment, Announcement, Teacher, Note
from django.views import generic
from application.forms import StudentForm, ParentSignUpForm, ClassComposeForm, ContentForm, PerformanceGradeForm, \
    AbsenceForm, AssignmentForm, TimetableForm, AnnouncementForm


# -----------------------------------------------------------------------------------------------
####### ADMINISTRATIVE OFFICER AREA##########
# -----------------------------------------------------------------------------------------------
class AdministrativeOfficer(generic.ListView):
    template_name = 'administrativeOfficer/aoAfterLogin.html'
    context_object_name = 'allClasses'

    def get_queryset(self):
        return ClassInfo.objects.all()


@login_required(login_url='application:login')
def timetable_form(request, name):
    if request.method == 'POST':
        instance = ClassInfo.objects.get(name=name)
        form = TimetableForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('application:administrativeOfficer')
    else:
        form = TimetableForm()
    return render(request, 'administrativeOfficer/chooseTimetable.html',
                  {'form': form, 'name': name, 'class': ClassInfo.objects.get(name=name)})


@login_required(login_url='application:login')
def enroll_student(request):
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
def class_compose(request):
    if request.method == 'POST':
        form = ClassComposeForm(request.POST)
        # form2 = ManualEnrollmentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            class_info = form.save()
            class_info.refresh_from_db()

            if Student.objects.filter(classID=None, studentYear='FIRST').count() < class_info.totalStudentsNumber:
                for student in Student.objects.filter(classID=None, studentYear='FIRST'):
                    student.classID = class_info
                    student.save()
            else:
                i = 0
                for student in Student.objects.filter(classID=None, studentYear='FIRST'):
                    if i < class_info.totalStudentsNumber:
                        i += 1
                        student.classID = class_info
                        student.save()

            messages.success(request, 'Class has been successfully added')

            # if form2.is_valid():
            #    form2.save()
            #   messages.success(request, 'Student has been assigned manually')

            return render(request, 'administrativeOfficer/classCompose.html',
                          {'form': form, 'numberOfSeats': number_of_seats(), 'numberOfStudents': number_of_students()})
    else:
        form = ClassComposeForm()
    # form2 = ManualEnrollmentForm()

    return render(request, 'administrativeOfficer/classCompose.html',
                  {'form': form, 'numberOfSeats': number_of_seats(), 'numberOfStudents': number_of_students()})


def number_of_seats():
    number = ClassInfo.objects.aggregate((Sum('totalStudentsNumber')))['totalStudentsNumber__sum']
    return number


def number_of_students():
    number = Student.objects.filter(classID=None).count()
    return number


@login_required(login_url='application:login')
def parent_signup(request):
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
                send_mail_to_parent(username, email, password)  # send credentials to a parent

                return render(request, 'administrativeOfficer/parentSignup.html', {'form': ParentSignUpForm()})
            else:
                return render(request, 'administrativeOfficer/parentSignup.html',
                              {'error_message': 'Invalid Information', 'form': ParentSignUpForm()})
    else:
        form = ParentSignUpForm()
    return render(request, 'administrativeOfficer/parentSignup.html', {'form': form})


@login_required(login_url='application:login')
def send_mail_to_parent(username, email, password):
    send_mail('School Account Credentials',
              'Dear Sir/Madam,\n We hope that this email finds you in a good health.\n' +
              'This is your credentials for accessing the school website\n' +
              'Username: ' + username + '\nPassword: ' + password + '\n' +
              'you can access our website by pressing this link: http://127.0.0.1:8000/application/login/' + '\n' +
              'Have a nice day.',
              'admofficer658@gmail.com',
              [email],
              fail_silently=False)


@login_required(login_url='application:login')
def communication_ao(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            new_announce = form.save()
            new_announce.save()
            messages.success(request, 'Announcement has benn sent successfully')
            return render(request, 'administrativeOfficer/communication.html', {'form': AnnouncementForm()})
    else:
        form = AnnouncementForm()

    return render(request, 'administrativeOfficer/communication.html', {'form': form})


class GetTeacherMasterData(generic.ListView):
    template_name = 'administrativeOfficer/teacherMasterData.html'
    context_object_name = 'allTeachers'

    def get_queryset(self):
        return Teacher.objects.all()


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


class AssignmentView(generic.ListView):
    template_name = 'parent/assignment.html'
    context_object_name = 'courseID'

    def get_queryset(self):
        return self.kwargs['courseID']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssignmentView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        if Assignment.objects.filter(courseID=self.kwargs['courseID']):
            context['assignments'] = Assignment.objects.filter(courseID=self.kwargs['courseID'])
        return context


class MaterialView(generic.ListView):
    template_name = 'parent/material.html'
    context_object_name = 'courseID'

    def get_queryset(self):
        return self.kwargs['courseID']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MaterialView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        allContent = Content.objects.filter(courseID=self.kwargs['courseID'])
        # check if there is any file uploaded yet in order to create material context
        if allContent:
            flag = 0
            for content in allContent:
                if content.material:
                    flag = 1
                    break
            if flag == 1:
                context['materials'] = Content.objects.filter(courseID=self.kwargs['courseID'])
        return context


class NotesView(generic.ListView):
    template_name = 'parent/note.html'
    context_object_name = 'notes'

    def get_queryset(self):
        studentCourseID = StudentCourse.objects.get(studentID=self.kwargs['studentID'],
                                                    courseID=self.kwargs['courseID'])
        return Note.objects.filter(studentCourseID=studentCourseID)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NotesView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['courseID'])
        context['courseID'] = self.kwargs['courseID']
        return context


class FinalGradeView(generic.ListView):
    template_name = 'parent/finalGrade.html'
    context_object_name = 'finalGrades'

    def get_queryset(self):
        return StudentCourse.objects.filter(studentID=self.kwargs['studentID'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FinalGradeView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        context['studentData'] = Student.objects.get(ID=self.kwargs['studentID'])
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
        for student_course in context['studentCourse']:
            grade_counter = 0
            for grade in context['allGrades']:
                if grade.studentCourseID.courseID.name == student_course.courseID.name:
                    grade_counter += 1
            if grade_counter > columns:
                columns = grade_counter
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


class AnnouncementView(generic.ListView):
    template_name = 'parent/announcement.html'
    context_object_name = 'allAnnouncements'

    def get_queryset(self):
        return Announcement.objects.all().order_by('-ID')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnnouncementView, self).get_context_data(**kwargs)
        context['studentID'] = self.kwargs['studentID']
        return context


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
def absence_form(request, courseID):
    student_courses = StudentCourse.objects.filter(courseID=courseID)
    n = student_courses.count()

    absence_formset = modelformset_factory(model=Attendance, form=AbsenceForm, extra=n, max_num=n)

    if request.method == 'POST':
        student_course = StudentCourse.objects.filter(courseID=courseID)
        absence_formset = absence_formset(request.POST, queryset=student_course)

        i = 0
        for f in absence_formset:
            if i < student_courses.count():
                f.studentCourseID = student_courses[i].studentID
                i += 1

        if absence_formset.is_valid():
            absence_formset.save()
            return render(request, 'teacher/absence.html', {'formset': absence_formset, 'courseID': courseID,
                                                            'date': str(datetime.date.today())})

    else:
        absence_formset = modelformset_factory(model=Attendance, form=AbsenceForm, extra=n, max_num=2)

    return render(request, 'teacher/absence.html', {'formset': absence_formset, 'courseID': courseID,
                                                    'date': str(datetime.date.today())})


@login_required(login_url='application:login')
def content_form(request, course_id):
    if request.method == 'POST':
        form = ContentForm(request.POST, user=request.user, request=request)
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.courseID = Course.objects.get(ID=course_id)
            unsaved_form.save()
            return redirect('application:teacher')
    else:
        form = ContentForm(user=request.user)
    return render(request, 'teacher/addTopicORMaterial.html', {'form': form, 'courseID': course_id, })


@login_required(login_url='application:login')
def grade_form(request, course_id):
    if request.method == 'POST':
        form = PerformanceGradeForm(request.POST, courseID=course_id)
        if form.is_valid():
            form.save()
            return redirect('application:teacher')
    else:
        form = PerformanceGradeForm(courseID=course_id)
    return render(request, 'teacher/grade.html', {'form': form, 'courseID': course_id, })


@login_required(login_url='application:login')
def assignment_form(request, course_id):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.courseID = Course.objects.get(ID=course_id)
            unsaved_form.save()
            return redirect('application:teacher')
    else:
        form = AssignmentForm()
    return render(request, 'teacher/addAssignment.html', {'form': form, 'courseID': course_id, })


class TeacherClassCoordinated(generic.ListView):
    template_name = 'teacher/coordinatedClass.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(classID=self.request.user.teacher.coordinatedClass)


class PutFinalGrade(generic.ListView):
    template_name = 'teacher/putfinalGrade.html'
    context_object_name = 'studentCourses'

    def get_queryset(self):
        return StudentCourse.objects.filter(studentID=self.kwargs['studentID'])


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


def login_user(request):
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
                        number_of_student = ParentStudent.objects.filter(parentID=parent.ID).count()

                        if parent.lastLogin is False:
                            parent.lastLogin = True
                            parent.save()
                            return redirect('application:change_password')
                        else:
                            if number_of_student == 1:
                                student_id = ParentStudent.objects.get(parentID=parent.ID).studentID.ID
                                return redirect('application:parentWithID', student_id)
                            else:
                                return redirect('application:chooseChild')
                    except:
                        try:
                            administrative_officer = user.administrativeofficer
                            return redirect('application:ao')
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
