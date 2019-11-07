from django.db import models
from AdministrativeOfficer.models import ClassInfo
from teacher.models import Course

# Create your models here.
class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    studentName = models.CharField(max_length=50)
    classID = models.ForeignKey(ClassInfo,on_delete=models.CASCADE)

class Parent(models.Model):
    parentID = models.AutoField(primary_key=True)
    fatherName = models.CharField(max_length=50)
    motherName = models.CharField(max_length=50)
    fatherEmail = models.EmailField
    motherName = models.EmailField
    fatherPassword = models.CharField(max_length=100)
    motherPassword = models.CharField(max_length=100)
    studentID = models.ForeignKey(Student,on_delete=models.CASCADE)

class StudentCourse(models.Model):
    ID = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student,on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course,on_delete=models.CASCADE)

class FinalGrade(models.Model):
    gradeID = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student,on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course,on_delete=models.CASCADE)
    finalGrade = models.IntegerField

#This class is used to record the weekly grades for the student throughout the year to measure the student performance

class performanceGrade(models.Model):
    gradeID = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField
    grade = models.IntegerField

    class Meta:
        unique_together = (("studentID", "courseID","date"),)