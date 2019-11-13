from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic

from application.forms import StudentForm


class TestView(generic.ListView):
    template_name = 'parent/afterloginparent.html'

    def get_queryset(self):
        return "salam"



class administrativeOfficer(generic.ListView):
    template_name = 'administrativeOfficer/base.html'

    def get_queryset(self):
        return "salam"


class IndexView(generic.ListView):
    template_name = 'application/index.html'

    def get_queryset(self):
        return "salam"


class LoginView(generic.ListView):
    template_name = 'application/login.html'

    def get_queryset(self):
        return "salam"


def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    teacher = user.teacher
                except:
                    try:
                        parent = user.parent
                        return redirect('application:test')
                    except:
                        try:
                            administrativeOfficer = user.administrativeofficer
                            return redirect('application:administrativeOfficer')
                        except:
                            try:
                                principle = user.principle
                                return HttpResponse("<h1>you are logged in as principle</h1>")
                            except:
                                return HttpResponse("<h1>you are a hacker</h1>")
        else:
            return render(request, 'application/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'application/login.html')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save();
            # redirect to a new URL:
            messages.success(request, 'Student has been successfully added')
            return render(request, 'application/signup.html', {'form': StudentForm()})

            # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'application/signup.html', {'form': form})
