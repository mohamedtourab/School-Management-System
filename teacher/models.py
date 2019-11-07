from django.db import models
import regex

from AdministrativeOfficer.models import ClassInfo

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
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    noteText = models.CharField(max_length=300)


class Content(models.Model):
    contentID = models.AutoField(primary_key=True)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    contentString = models.CharField(max_length=100)


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    fiscalCode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    coursesTaught = models.ForeignKey(Course, on_delete=models.CASCADE)  # FIX THAT
    coordinatedClass = models.ForeignKey(ClassInfo, null=True, blank=True)


class FreeSlots(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # check ONDELETE
    date = models.DateField
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


class Attendance(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    presence = models.BooleanField(default=True)
    date = models.DateField
    came_late = models.BooleanField(default=False)
    left_early = models.BooleanField(default=False)
