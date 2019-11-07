from django.db import models
from parent.models import Student


# Create your models here.
class Course(models.Model):
    courseID = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=50)
    numberOfHoursPerWeek = models.PositiveIntegerField
    year = models.CharField(max_length=10)
    assignment = models.FileField;


class Note(models.Model):
    noteID = models.AutoField(primary_key=True)
    courseID = models.ForeignKey(Course,on_delete=models.CASCADE)
    studentID = models.ForeignKey(Student,on_delete=models.CASCADE)
    noteText = models.CharField(max_length=300)

class Content(models.Model):
    contentID = models.AutoField(primary_key=True)
    courseID = models.ForeignKey(Course,on_delete=models.CASCADE)
    contentString = models.CharField(max_length=100)
