from django.db import models

# Create your models here.
#There is a missing field which is the TimeTable field to be done later
#TODO add TimeTable field for the class

class ClassInfo(models.Model):
    classID = models.AutoField(primary_key=True)
    className = models.CharField(max_length=30)
    totalStudentsNumber= models.PositiveIntegerField
