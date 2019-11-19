from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Student, ClassInfo, Content, TeacherCourse


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
    class Meta:
        model = Content
        fields = ['courseID', 'contentString', 'material']

# class ContentForm(ModelForm):
#     courseID = None
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         self.courseID = forms.ModelChoiceField(queryset=TeacherCourse.objects.filter(teacherID=self.user.teacher.ID),
#                                                initial=self.courseID)
#         super(ContentForm, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = Content
#         fields = ['courseID', 'contentString', 'material']
