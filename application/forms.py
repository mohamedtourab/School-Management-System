from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory, formset_factory
import datetime

from .models import Student, ClassInfo, Content, TeacherCourse, Course, PerformanceGrade, StudentCourse, Attendance, \
    Assignment, Announcement, Teacher, AssignFinalGrade


class AnnouncementForm(ModelForm):
    announcementText = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Announcement
        fields = ['announcementTitle', 'announcementText', 'date']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'classID', 'studentYear']


class ParentSignUpForm(UserCreationForm):
    studentID = forms.ModelMultipleChoiceField(queryset=Student.objects.all())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'studentID',)


class TeacherCreateForm(UserCreationForm):
    coordinatedClass = forms.ModelMultipleChoiceField(queryset=ClassInfo.objects.all(), required=False)
    fiscalCode = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'fiscalCode',
                  'coordinatedClass', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(TeacherCreateForm, self).save(commit=False)
        user.coordinatedClass = self.cleaned_data["fiscalCode"]
        if commit:
            user.save()
        return user


class ClassComposeForm(ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['ID', 'name', 'totalStudentsNumber']


class ContentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.request = kwargs.pop('request', None)
        super(ContentForm, self).__init__(*args, **kwargs)
        # listOfCoursesID = (TeacherCourse.objects.filter(teacherID=self.user.teacher.ID)).values('course_id')
        # listOfCourses = Course.objects.filter(ID__in=listOfCoursesID)
        # self.course_id = forms.ModelChoiceField(queryset=listOfCourses)
        # self.fields['course_id'] = self.course_id

    def clean(self):
        cleaned_data = super().clean()
        material_title = cleaned_data.get("material_title")
        material_file = self.request.POST.get('material')
        content_string = cleaned_data.get("contentString")
        if not content_string:
            if (not material_file) and (not material_title):
                # Only do something if both fields are not valid so far.
                raise forms.ValidationError(
                    "You have to submit either Topic Title or File and File title"
                )
            elif not material_title:
                raise forms.ValidationError(
                    "File title is missing"
                )
            elif not material_file:
                raise forms.ValidationError(
                    "File is missing"
                )

    class Meta:
        model = Content
        exclude = ('course_id',)
        fields = ['contentString', 'materialTitle', 'material', ]


class PerformanceGradeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id', None)
        super(PerformanceGradeForm, self).__init__(*args, **kwargs)
        self.studentCourseID = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(course_id=self.course_id))
        self.fields['studentCourseID'] = self.studentCourseID

    class Meta:
        model = PerformanceGrade
        fields = ['studentCourseID', 'date', 'grade', ]


def to_integer(dt_time):
    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day


class AbsenceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id', None)
        super(AbsenceForm, self).__init__(*args, **kwargs)
        self.studentCourseID = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(course_id=self.course_id))
        self.fields['studentCourseID'] = self.studentCourseID

        self.date = datetime.date.today


    class Meta:
        model = Attendance
        fields = ['studentCourseID', 'date', 'presence', 'cameLate', 'leftEarly']


class BehaviorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id', None)
        self.date = datetime.date.today
        self.ID = to_integer(datetime.date.today())
        super(BehaviorForm, self).__init__(*args, **kwargs)

        self.studentCourseID = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(),
                                                      initial=StudentCourse.objects.filter(course_id=self.course_id))
        self.fields['studentCourseID'] = self.studentCourseID

    class Meta:
        model = Attendance
        fields = ['ID', 'studentCourseID', 'date', 'behavior']



class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ('course_id', 'additionDate', 'fileName',)
        fields = ['assignmentTitle', 'assignmentFile', 'deadlineDate']


class TimetableForm(ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['timetable']


class AppointmentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.teacherID = kwargs.pop('teacherID', None)
        super(AppointmentsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Teacher
        exclude = ['first_name', 'fiscalCode', 'last_name', 'coordinatedClass', 'email', 'user']
        fields = ['appointmentSchedule']


class PutFinalGradeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.studentID = kwargs.pop('studentID', None)
        super(PutFinalGradeForm, self).__init__(*args, **kwargs)
        self.student_course = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(studentID=self.studentID))
        self.fields['student_course'] = self.student_course

    class Meta:
        model = AssignFinalGrade
        fields = ['student_course', 'final_grade', ]