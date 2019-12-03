from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory, formset_factory
import datetime

from .models import Student, ClassInfo, Content, TeacherCourse, Course, PerformanceGrade, StudentCourse, Attendance, \
    Assignment


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


# class ManualEnrollmentForm(ModelForm):
#     def getListOfFreeClasses(self):
#         studentList = Student.objects.filter(studentYear='FIRST')
#         classInformation = dict()
#         for student in studentList:
#             if (classInformation.get(student.classID.name) != None):
#                 classInformation[student.classID.name] = classInformation.get(student.classID.name) + 1
#             else:
#                 classInformation[student.classID.name] = 1
#         listOfClassNames = []
#         for key, value in classInformation.items():
#             classDetails = ClassInfo.objects.get(name=key)
#             if (classDetails.totalStudentsNumber > value):
#                 listOfClassNames.append(key)
#
#     classes = forms.ModelChoiceField(queryset=ClassInfo.objects.all())
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(ManualEnrollmentForm, self).__init__(*args, **kwargs)
#         self.classes = forms.ModelChoiceField(queryset=ClassInfo.objects.filter(name__in=self.getListOfFreeClasses()))
#
#     student = forms.ModelMultipleChoiceField(queryset=Student.objects.filter(classID__isnull=True))
#
#     class Meta:
#         model = Student
#         exclude = ['ID']
#         fields = ['classes', 'student']


class ContentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContentForm, self).__init__(*args, **kwargs)
        # listOfCoursesID = (TeacherCourse.objects.filter(teacherID=self.user.teacher.ID)).values('courseID')
        # listOfCourses = Course.objects.filter(ID__in=listOfCoursesID)
        # self.courseID = forms.ModelChoiceField(queryset=listOfCourses)
        # self.fields['courseID'] = self.courseID

    class Meta:
        model = Content
        exclude = ('courseID',)
        fields = ['contentString', 'material', ]


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
        self.studentCourseID = forms.ModelChoiceField(queryset=StudentCourse.objects.filter(courseID=self.courseID))
        self.date = forms.DateField(initial=datetime.date.today)
        self.fields['studentCourseID'] = self.studentCourseID
        self.fields['date'] = self.date

    class Meta:
        model = Attendance
        fields = ['ID', 'studentCourseID', 'date', 'presence', 'cameLate', 'leftEarly', ]


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ('courseID', 'additionDate', 'fileName',)
        fields = ['assignmentTitle', 'assignmentFile', 'deadlineDate']


class TimetableForm(ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['timetable']
