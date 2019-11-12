from django.contrib import admin
from .models import Teacher,Principle,Parent,AdministrativeOfficer,Student,ClassInfo,StudentCourse, Course

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Principle)
admin.site.register(Parent)
admin.site.register(AdministrativeOfficer)
admin.site.register(Student)
admin.site.register(ClassInfo)
admin.site.register(StudentCourse)
admin.site.register(Course)