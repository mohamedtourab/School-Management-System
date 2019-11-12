from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Student

class StudentForm(ModelForm):
    class Meta:
        fields = ['Name','surname','classID','studentYear']
