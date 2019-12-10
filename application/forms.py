from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory, formset_factory
import datetime

from .models import Student, ClassInfo, Content, TeacherCourse, Course, PerformanceGrade, StudentCourse, Attendance, \
    Assignment, Announcement


class AnnouncementForm(ModelForm):
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


class ClassComposeForm(ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['ID', 'name', 'totalStudentsNumber']


class ContentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.request = kwargs.pop('request', None)
        super(ContentForm, self).__init__(*args, **kwargs)
        # listOfCoursesID = (TeacherCourse.objects.filter(teacherID=self.user.teacher.ID)).values('courseID')
        # listOfCourses = Course.objects.filter(ID__in=listOfCoursesID)
        # self.courseID = forms.ModelChoiceField(queryset=listOfCourses)
        # self.fields['courseID'] = self.courseID

    def clean(self):
        cleaned_data = super().clean()
        materialTitle = cleaned_data.get("materialTitle")
        materialFile = self.request.POST.get('material')
        contentString = cleaned_data.get("contentString")
        if (not contentString):
            if ((not materialFile) and (not materialTitle)):
                # Only do something if both fields are not valid so far.
                raise forms.ValidationError(
                    "You have to submit either Topic Title or File and File title"
                )
            elif not materialTitle:
                raise forms.ValidationError(
                    "File title is missing"
                )
            elif not materialFile:
                raise forms.ValidationError(
                    "File is missing"
                )
    class Meta:
        model = Content
        exclude = ('courseID',)
        fields = ['contentString', 'materialTitle', 'material',]


class PerformanceGradeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.courseID = kwargs.pop('courseID', None)
        super(PerformanceGradeForm, self).__init__(*args, **kwargs)
        self.studentCourseID = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(courseID=self.courseID))
        self.fields['studentCourseID'] = self.studentCourseID

    class Meta:
        model = PerformanceGrade
        fields = ['studentCourseID', 'date', 'grade', ]


class AbsenceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.courseID = kwargs.pop('courseID', None)
        super(AbsenceForm, self).__init__(*args, **kwargs)

        self.studentCourseID = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(),
                                                      initial=StudentCourse.objects.filter(courseID=self.courseID))
        self.date = forms.DateField(initial=datetime.date.today)
        self.fields['studentCourseID'] = self.studentCourseID
        self.fields['date'] = self.date

    class Meta:
        model = Attendance
        fields = ['ID', 'studentCourseID', 'date', 'presence', 'cameLate', 'leftEarly', 'behaviour']


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ('courseID', 'additionDate', 'fileName',)
        fields = ['assignmentTitle', 'assignmentFile', 'deadlineDate']


class TimetableForm(ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['timetable']
