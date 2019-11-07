from django.db import models


# Create your models here.

class AdministrativeOfficer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Announcements(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    announcementText = models.CharField(max_length=500)


# There is a missing field which is the TimeTable field to be done later
# TODO add TimeTable field for the class

class ClassInfo(models.Model):
    classID = models.AutoField(primary_key=True)
    className = models.CharField(max_length=30)
    totalStudentsNumber = models.PositiveIntegerField
