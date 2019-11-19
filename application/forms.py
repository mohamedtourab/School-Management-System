from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Student, ClassInfo, Content, TeacherCourse, Course


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'classID', 'studentYear']


class ParentSignUpForm(UserCreationForm):
    studentID = forms.ModelChoiceField(queryset=Student.objects.all())

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
        listOfCoursesID = (TeacherCourse.objects.filter(teacherID=self.user.teacher.ID)).values('courseID')
        listOfCourses = Course.objects.filter(ID__in=listOfCoursesID)
        self.courseID = forms.ModelChoiceField(queryset=listOfCourses)
        super(ContentForm, self).__init__(*args, **kwargs)
        self.fields['courseID'] = self.courseID

    class Meta:
        model = Content
        fields = ['courseID', 'contentString', 'material', ]
