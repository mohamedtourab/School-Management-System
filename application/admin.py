from django.contrib import admin
from .models import Teacher,Principle,Parent,AdministrativeOfficer

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Principle)
admin.site.register(Parent)
admin.site.register(AdministrativeOfficer)

