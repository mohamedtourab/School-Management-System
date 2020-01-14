from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
import csv
from functools import partial, wraps
from django.forms import formset_factory
from .models import StudentCourse, PerformanceGrade, Parent, Content, Course, Student, ClassInfo, TeacherCourse, \
    ParentStudent, Attendance, Assignment, Announcement, Teacher, Note, Behavior, ClassCourse
from django.views import generic
from application.forms import StudentForm, ParentSignUpForm, ClassComposeForm, ContentForm, PerformanceGradeForm, \
    AbsenceForm, AssignmentForm, TimetableForm, AnnouncementForm, TeacherCreateForm, AppointmentsForm, \
    PutFinalGradeForm, BehaviorForm


# -----------------------------------------------------------------------------------------------
####### HELPER FUNCTIONS AREA##########
# -----------------------------------------------------------------------------------------------
def read_csv_file(file, dictionary, used_delimiter):
    csv_file = open(file.path, 'r')
    read_csv = csv.reader(csv_file, delimiter=used_delimiter)
    first = 1
    index = 0
    for row in read_csv:
        if first == 1:
            first = 0
            dictionary.update({'header0': row[0]})
            dictionary.update({'header1': row[1]})
            dictionary.update({'header2': row[2]})
            dictionary.update({'header3': row[3]})
            dictionary.update({'header4': row[4]})
            dictionary.update({'header5': row[5]})
        else:
            dictionary.update({'row' + str(index) + '0': row[0]})
            dictionary.update({'row' + str(index) + '1': row[1]})
            dictionary.update({'row' + str(index) + '2': row[2]})
            dictionary.update({'row' + str(index) + '3': row[3]})
            dictionary.update({'row' + str(index) + '4': row[4]})
            dictionary.update({'row' + str(index) + '5': row[5]})
            index += 1


def number_of_seats():
    number = ClassInfo.objects.aggregate((Sum('totalStudentsNumber')))['totalStudentsNumber__sum']
    return number


def number_of_students():
    number = Student.objects.filter(classID=None).count()
    return number


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
            return redirect('application:ao')
    else:
        form = TimetableForm()

    my_dict = {'class': ClassInfo.objects.filter(name=name)}  # GET CLASS NAME
    if ClassInfo.objects.filter(name=name).exists():
        my_dict.update({'class': ClassInfo.objects.get(name=name)})
    my_dict.update({'name': name})
    timetable = my_dict['class'].timetable
    try:
        read_csv_file(file=timetable, dictionary=my_dict, used_delimiter=',')
        my_dict.update({'class': 'timetable'})
    except:
        pass
    return render(request, 'administrativeOfficer/chooseTimetable.html',
                  {'form': form, 'name': name, 'my_dict': my_dict, 'class': ClassInfo.objects.get(name=name)})


@login_required(login_url='application:login')
def enroll_student(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        try:
            user = User.objects.get(username=request.POST['username'], )
            return render(request, 'administrativeOfficer/enrollStudent.html',
                          {'error_message': 'Username already Exist.\nTry another Username.', 'form': StudentForm()})
        except User.DoesNotExist:
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                student = Student.objects.create(user=user, studentYear=form['student_year'].value())
            messages.success(request, 'Student has been successfully added')
            return render(request, 'administrativeOfficer/enrollStudent.html', {'form': StudentForm()})
            # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()
    return render(request, 'administrativeOfficer/enrollStudent.html', {'form': form})


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
                for student in form.cleaned_data.get('student_id'):
                    ParentStudent.objects.create(student_id=student, parentID=parent)

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
def class_compose(request):
    if request.method == 'POST':
        form = ClassComposeForm(request.POST)
        if form.is_valid():
            class_info = form.save()
            class_info.refresh_from_db()
            if class_info.name[0] == '1':
                course1 = Course.objects.get_or_create(name='Math 1', numberOfHoursPerWeek='10', year='FIRST')
                course2 = Course.objects.get_or_create(name='Physics 1', numberOfHoursPerWeek='10', year='FIRST')
                course3 = Course.objects.get_or_create(name='English', numberOfHoursPerWeek='10', year='FIRST')
                ClassCourse.objects.get_or_create(class_id=class_info, course_id=course1[0],
                                                  teacher_id=Teacher.objects.get(first_name='Marco'))
                ClassCourse.objects.get_or_create(class_id=class_info, course_id=course2[0],
                                                  teacher_id=Teacher.objects.get(first_name='Marco'))
                ClassCourse.objects.get_or_create(class_id=class_info, course_id=course3[0],
                                                  teacher_id=Teacher.objects.get(first_name='Marco'))

            elif class_info.name[0] == '2':
                course1, create1 = Course.objects.get_or_create(name='Math 2', numberOfHoursPerWeek='10', year='SECOND')
                course2, create2 = Course.objects.get_or_create(name='Physics 2', numberOfHoursPerWeek='10',
                                                                year='SECOND')
                course3, create3 = Course.objects.get_or_create(name='Italian', numberOfHoursPerWeek='10',
                                                                year='SECOND')
                ClassCourse.objects.get_or_create(class_id=class_info, course_id=course1,
                                                  teacher_id=Teacher.objects.get(first_name='Antonio'))
                ClassCourse.objects.get_or_create(class_id=class_info, course_id=course2,
                                                  teacher_id=Teacher.objects.get(first_name='Antonio'))
                ClassCourse.objects.get_or_create(class_id=class_info, course_id=course3,
                                                  teacher_id=Teacher.objects.get(first_name='Antonio'))
            first_year_courses = Course.objects.filter(year='FIRST')
            if Student.objects.filter(classID=None, studentYear='FIRST').count() < class_info.totalStudentsNumber:
                for student in Student.objects.filter(classID=None, studentYear='FIRST'):
                    student.classID = class_info
                    student.save()
                    for course in first_year_courses:
                        StudentCourse.objects.create(student_id=student, course_id=course)
            else:
                i = 0
                for student in Student.objects.filter(classID=None, studentYear='FIRST'):
                    if i < class_info.totalStudentsNumber:
                        i += 1
                        student.classID = class_info
                        student.save()
                        for course in first_year_courses:
                            StudentCourse.objects.create(student_id=student, course_id=course)

            messages.success(request, 'Class has been successfully added')
            return render(request, 'administrativeOfficer/classCompose.html',
                          {'form': form, 'numberOfSeats': number_of_seats(), 'numberOfStudents': number_of_students()})
    else:
        form = ClassComposeForm()
    return render(request, 'administrativeOfficer/classCompose.html',
                  {'form': form, 'numberOfSeats': number_of_seats(), 'numberOfStudents': number_of_students()})


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


class EditTeacherMasterData(UpdateView):
    template_name = 'administrativeOfficer/teacher-form.html'
    model = Teacher
    fields = ['first_name', 'last_name', 'email', 'fiscalCode', 'coordinatedClass']


class DeleteTeacherMasterData(DeleteView):
    model = Teacher

    def get_success_url(self):
        return reverse('application:teacherMasterData')


@login_required(login_url='application:login')
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        try:
            if Teacher.objects.get(fiscalCode=form['fiscalCode'].value()):
                return render(request, 'administrativeOfficer/teacherCreate.html',
                              {'error_message': 'Fiscal Code Exist...Try Something Else !',
                               'form': TeacherCreateForm()})
        except:
            try:
                user = User.objects.get(username=request.POST['username'], )
                return render(request, 'administrativeOfficer/teacherCreate.html',
                              {'error_message': 'Username Exist...Try Something Else !', 'form': TeacherCreateForm()})
            except User.DoesNotExist:
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()  # load the profile instance created by the signal
                    teacher = Teacher.objects.create(user=user, first_name=user.first_name, last_name=user.last_name,
                                                     email=user.email, fiscalCode=request.POST['fiscalCode'], )

                    messages.success(request, 'Teacher has been successfully added')

                    return render(request, 'administrativeOfficer/teacherCreate.html', {'form': TeacherCreateForm()})
                else:
                    return render(request, 'administrativeOfficer/teacherCreate.html',
                                  {'error_message': 'Invalid Information', 'form': TeacherCreateForm()})
    else:
        form = TeacherCreateForm()
        return render(request, 'administrativeOfficer/teacherCreate.html', {'form': form})


# -----------------------------------------------------------------------------------------------
####### PARENT AREA##########
# -----------------------------------------------------------------------------------------------

class TestView(generic.ListView):
    template_name = 'parent/afterloginparent.html'

    def get_queryset(self):
        return "salam"


class CourseView(generic.ListView):
    template_name = 'parent/course.html'
    context_object_name = 'student_id'

    def get_queryset(self):
        return self.kwargs['student_id']


@login_required(login_url='application:login')
def parent_view(request, student_id):
    my_dict = {'allStudentCourses': Course.objects.filter(studentcourse__student_id=student_id)}  # GET STUDENT ID HERE
    my_dict.update({'parentStudent': ParentStudent.objects.filter(student_id=student_id)})
    my_dict.update({'student_id': student_id})
    if ClassInfo.objects.filter(student__ID=student_id).exists():
        my_dict.update({'studentClass': ClassInfo.objects.get(student__ID=student_id)})
        timetable = my_dict['studentClass'].timetable
        try:
            read_csv_file(file=timetable, dictionary=my_dict, used_delimiter=',')
            my_dict.update({'timeTable': 'timetable'})
        except:
            pass
    return render(request, 'parent/afterloginparent.html', my_dict)


class ChooseChild(generic.ListView):
    template_name = 'parent/chooseChild.html'
    context_object_name = 'allChildren'

    def get_queryset(self):
        return ParentStudent.objects.filter(parentID=self.request.user.parent.ID)  # GET STUDENT ID HERE


class ParentAttendanceView(generic.ListView):
    template_name = 'parent/attendancep.html'
    context_object_name = 'student_id'

    def get_queryset(self):
        return self.kwargs['student_id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentAttendanceView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['attendances'] = Attendance.objects.filter(Q(studentCourseID__student_id=self.kwargs['student_id']),
                                                           Q(studentCourseID__course_id=self.kwargs[
                                                               'course_id']), ).order_by('date')
        # create new Vew for handling attendance divided into months, need to add new constraint to the query,
        # and send Month_Name into next url
        return context


class ParentBehaviorView(generic.ListView):
    template_name = 'parent/behaviorp.html'
    context_object_name = 'student_id'

    def get_queryset(self):
        return self.kwargs['student_id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentBehaviorView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['behavior'] = Behavior.objects.filter(Q(studentCourseID__student_id=self.kwargs['student_id']),
                                                      Q(studentCourseID__course_id=self.kwargs[
                                                          'course_id']), ).order_by('-ID')
        # create new Vew for handling attendance divided into months, need to add new constraint to the query,
        # and send Month_Name into next url
        return context


class CourseDetailView(generic.ListView):
    template_name = 'parent/course.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Content.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['course_id'])
        context['course_id'] = self.kwargs['course_id']
        return context


class AssignmentView(generic.ListView):
    template_name = 'parent/assignment.html'
    context_object_name = 'course_id'

    def get_queryset(self):
        return self.kwargs['course_id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssignmentView, self).get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        if Assignment.objects.filter(course_id=self.kwargs['course_id']):
            context['assignments'] = Assignment.objects.filter(course_id=self.kwargs['course_id'])
        return context


class MaterialView(generic.ListView):
    template_name = 'parent/material.html'
    context_object_name = 'course_id'

    def get_queryset(self):
        return self.kwargs['course_id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MaterialView, self).get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        all_content = Content.objects.filter(course_id=self.kwargs['course_id'])
        # check if there is any file uploaded yet in order to create material context
        if all_content:
            flag = 0
            for content in all_content:
                if content.material:
                    flag = 1
                    break
            if flag == 1:
                context['materials'] = Content.objects.filter(course_id=self.kwargs['course_id'])
        return context


class NotesView(generic.ListView):
    template_name = 'parent/note.html'
    context_object_name = 'notes'

    def get_queryset(self):
        student_course_id = StudentCourse.objects.get(student_id=self.kwargs['student_id'],
                                                      course_id=self.kwargs['course_id'])
        return Note.objects.filter(studentCourseID=student_course_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NotesView, self).get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['course_id'])
        context['course_id'] = self.kwargs['course_id']
        return context


class FinalGradeView(generic.ListView):
    template_name = 'parent/finalGrade.html'
    context_object_name = 'finalGrades'

    def get_queryset(self):
        return StudentCourse.objects.filter(student_id=self.kwargs['student_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FinalGradeView, self).get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        context['studentData'] = Student.objects.get(ID=self.kwargs['student_id'])
        return context


class ParentGradeView(generic.ListView):
    template_name = 'parent/gradep.html'
    context_object_name = 'allGrades'

    def get_queryset(self):
        return PerformanceGrade.objects.filter(studentCourseID__student_id=self.kwargs[
            'student_id'])  # GET STUDENTcourse_id HERE ; should I send student_id to the url here?

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ParentGradeView, self).get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        context['studentCourse'] = StudentCourse.objects.filter(
            student_id=self.kwargs['student_id'])  # GET STUDENT ID HERE

        columns = 0
        for student_course in context['studentCourse']:
            grade_counter = 0
            for grade in context['allGrades']:
                if grade.studentCourseID.course_id.name == student_course.course_id.name:
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
        context['student_id'] = self.kwargs['student_id']
        return context


# -----------------------------------------------------------------------------------------------
####### TEACHER AREA##########
# -----------------------------------------------------------------------------------------------

class TeacherView(generic.ListView):
    template_name = 'teacher/teacherAfterLogin.html'
    context_object_name = 'allTeacherCourses'

    def get_queryset(self):
        return TeacherCourse.objects.filter(teacherID=self.request.user.teacher.ID)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherView, self).get_context_data(**kwargs)
        context['teacherID'] = self.request.user.teacher.ID
        context['coordinatedClass'] = Teacher.objects.get(ID=self.request.user.teacher.ID).coordinatedClass
        return context


class AppointmentView(generic.ListView):
    template_name = 'teacher/appointment.html'
    context_object_name = 'teacherID'

    def get_queryset(self):
        return self.request.user.teacher.ID


def appointment_form(request, teacher_id):
    my_dict = {
        'teacher': Teacher.objects.get(ID=teacher_id)}  # GET STUDENT ID HERE
    appointment_schedule = my_dict['teacher'].appointmentSchedule
    try:
        read_csv_file(file=appointment_schedule, dictionary=my_dict, used_delimiter=';')
        my_dict.update({'AS': 'appointment_schedule'})
    except:
        pass

    if request.method == 'POST':
        instance = Teacher.objects.get(ID=teacher_id)
        form = AppointmentsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('application:teacher')
    else:
        form = AppointmentsForm()

    return render(request, 'teacher/appointment.html', {'form': form, 'teacherID': teacher_id, 'my_dict': my_dict})


class TimetablesView(generic.ListView):
    template_name = 'teacher/timetables.html'
    context_object_name = 'teacherID'

    def get_queryset(self):
        return self.request.user.teacher.ID

class TimetablesWithIDView(generic.ListView):
    template_name = 'teacher/timetables.html'
    context_object_name = 'teacher_id'

    def get_queryset(self):
        return self.request.user.teacher.ID

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TimetablesWithIDView, self).get_context_data(**kwargs)
        context['classes'] = ClassCourse.objects.filter(teacher_id=self.kwargs['teacher_id'])
        return context


def timetables_specific_class_view(request, class_id, course_id):
    my_dict = {'course' : course_id}
    my_dict.update({'class_id': class_id})
    timetable = my_dict['course'].timetable
    try:
        read_csv_file(file=timetable, dictionary=my_dict, used_delimiter=',')
        my_dict.update({'timeTable': 'timetable'})
    except:
        pass
    return render(request, 'parent/afterloginparent.html', my_dict)


class TeacherCourseDetailView(generic.ListView):
    template_name = 'teacher/course.html'
    context_object_name = 'contents'

    def get_queryset(self):
        return Content.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherCourseDetailView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['course_id'])
        context['assignments'] = Assignment.objects.filter(course_id=self.kwargs['course_id'])
        return context


class AbsenceView(generic.ListView):
    template_name = 'teacher/absence.html'
    context_object_name = 'absence'

    def get_queryset(self):
        return Content.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AbsenceView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['course_id'])
        return context


class BehaviorView(generic.ListView):
    template_name = 'teacher/behavior.html'
    context_object_name = 'behavior'

    def get_queryset(self):
        return Content.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BehaviorView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['courseDetails'] = Course.objects.get(ID=self.kwargs['course_id'])
        return context


@login_required(login_url='application:login')
def absence_form(request, course_id):
    if request.method == 'POST':
        form = AbsenceForm(request.POST, course_id=course_id)
        if form.is_valid():
            unsaved_form = form.save()
            unsaved_form.save()
            return render(request, 'teacher/absence.html', {'form': form, 'course_id': course_id})
    else:
        form = AbsenceForm(course_id=course_id)
    return render(request, 'teacher/absence.html', {'form': form, 'course_id': course_id})


@login_required(login_url='application:login')
def behavior_form(request, course_id):
    if request.method == 'POST':
        form = BehaviorForm(request.POST, course_id=course_id)
        if form.is_valid():
            unsaved_form = form.save()
            unsaved_form.save()
            return render(request, 'teacher/behavior.html', {'form': form, 'course_id': course_id})
    else:
        form = BehaviorForm(course_id=course_id)
    return render(request, 'teacher/behavior.html', {'form': form, 'course_id': course_id})


@login_required(login_url='application:login')
def content_form(request, course_id):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, user=request.user, request=request)
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.course_id = Course.objects.get(ID=course_id)
            unsaved_form.save()
            return redirect('application:teacher')
    else:
        form = ContentForm(user=request.user)
    return render(request, 'teacher/addTopicORMaterial.html', {'form': form, 'course_id': course_id, })


@login_required(login_url='application:login')
def grade_form(request, course_id):
    if request.method == 'POST':
        form = PerformanceGradeForm(request.POST, course_id=course_id)
        if form.is_valid():
            form.save()
            return redirect('application:teacher')
    else:
        form = PerformanceGradeForm(course_id=course_id)
    return render(request, 'teacher/grade.html', {'form': form, 'course_id': course_id, })


@login_required(login_url='application:login')
def assignment_form(request, course_id):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            unsaved_form = form.save(commit=False)
            unsaved_form.course_id = Course.objects.get(ID=course_id)
            unsaved_form.save()
            return redirect('application:teacher')
    else:
        form = AssignmentForm()
    return render(request, 'teacher/addAssignment.html', {'form': form, 'course_id': course_id, })


class TeacherClassCoordinated(generic.ListView):
    template_name = 'teacher/coordinatedClass.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(classID=self.request.user.teacher.coordinatedClass)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherClassCoordinated, self).get_context_data(**kwargs)
        context['studentCourse'] = StudentCourse.objects.filter(
            student_id__classID=self.request.user.teacher.coordinatedClass)
        return context


@login_required(login_url='application:login')
def final_grade_form(request, student_id):
    if request.method == 'POST':
        form = PutFinalGradeForm(request.POST, student_id=student_id)
        if form.is_valid():
            form.save()
            sc_fk = request.POST['student_course']
            sc = StudentCourse.objects.filter(pk__in=sc_fk).all()
            for sc_obj in sc:
                if sc_obj.publishFinalGrade:
                    return render(request, 'teacher/final_grade.html',
                                  {
                                      'error_message': 'Final grade for the student of this course has been already assigned!',
                                      'form': form, 'student_id': student_id, })
                else:
                    sc.update(finalGrade=request.POST['final_grade'])
                    sc.update(publishFinalGrade=True)
                    return redirect('application:TeacherCoordinator')
    else:
        form = PutFinalGradeForm(student_id=student_id)
    return render(request, 'teacher/final_grade.html', {'form': form, 'student_id': student_id, })


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
                                student_id = ParentStudent.objects.get(parentID=parent.ID).student_id.ID
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
                                try:
                                    student = user.student
                                    return redirect('application:student_login_view', user.student.ID)
                                except:
                                    return HttpResponse("<h1>you are a hacker</h1>")
        else:
            return render(request, 'application/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'application/login.html')


# -----------------------------------------------------------------------------------------------
####### STUDENT AREA##########
# -----------------------------------------------------------------------------------------------
def student_login_view(request, student_id):
    return HttpResponse("<h1>you are a student</h1>")
