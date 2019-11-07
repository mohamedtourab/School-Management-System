from django.db import models

# Create your models here.

class AdministrativeOfficer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

class Announcements(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    announcementText = models.CharField(max_length=500)

