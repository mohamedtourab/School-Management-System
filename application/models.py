from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Principle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.user.username


class AdministrativeOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.user.username


# There is a missing field which is the TimeTable field to be done later
# TODO add TimeTable field for the class
class ClassInfo(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    totalStudentsNumber = models.PositiveIntegerField()


class Student(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, verbose_name='First Name')
    surname = models.CharField(max_length=50, verbose_name='Last Name')
    classID = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, verbose_name='Student Class Name', blank=True,
                                null=True)
    studentYear = models.CharField(max_length=20, verbose_name='Year Grade')


class Course(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    numberOfHoursPerWeek = models.PositiveIntegerField()
    year = models.CharField(max_length=10)
    assignment = models.FileField(blank=True, null=True)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)
    fiscalCode = models.CharField(max_length=16)
    coordinatedClass = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username


class TeacherCourse(models.Model):
    ID = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class PerformanceGrade(models.Model):
    ID = models.AutoField(primary_key=True)
    studentCourseID = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    grade = models.PositiveIntegerField()


class StudentCourse(models.Model):
    ID = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    finalGrade = models.PositiveIntegerField(blank=True, null=True)


class Note(models.Model):
    ID = models.AutoField(primary_key=True)
    studentCourseID = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    noteText = models.CharField(max_length=300)


class Content(models.Model):
    ID = models.AutoField(primary_key=True)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    contentString = models.CharField(max_length=100)


class Announcements(models.Model):
    ID = models.AutoField(primary_key=True)
    announcementText = models.CharField(max_length=500)


class Attendance(models.Model):
    ID = models.AutoField(primary_key=True)
    studentCourseID = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    presence = models.BooleanField(default=True)
    date = models.DateField()
    cameLate = models.BooleanField(default=False)
    leftEarly = models.BooleanField(default=False)


class FreeSlots(models.Model):
    teacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # check ONDELETE
    date = models.DateField()
    schedule = models.CharField(max_length=24)  # we have 24 slots (6 hours per day, 4 slots per hour, 15 mins each)

    def time_slot_to_regex(self, start_time, end_time):
        # times should be in HH:MM format
        start_hour, start_minutes = start_time.split(':')
        end_hour, end_minutes = end_time.split(':')

        slots_before_needed_time = (int(start_hour) * 4 + int(start_minutes) / 15)

        # compute how many hours are between given times and find out nr of slots
        hour_duration_slots = (int(end_hour) - int(start_hour)) * 4  # 4 slots in each hour

        # adjust nr of slots according to minutes in provided times.
        # e.g. 9:30 to 10:45 - we have 10-9=1 hour, which is 4 time slots,
        # but we need to subtract 2 time slots, because we don't have 9:00 to 10:00,
        # but 9:30 to 10:00 so we subtract 30/15=2 timeslots and add what is left
        # from the incomplete hour of 10:45 time, which is 45/15 minutes = 3 slots
        minute_duration_slots = int(end_minutes) / 15 - int(start_minutes) / 15

        total_duration = hour_duration_slots + minute_duration_slots

        regular_expression = r'^[01]{%d}1{%d}' % (slots_before_needed_time, total_duration)

        return regular_expression

    #  Function to use to find who's available within a specific time slot
    #       DailySchedule.objects.filter(date=date, schedule__regex=r'<expression>')
