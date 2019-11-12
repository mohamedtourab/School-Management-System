from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic


class TestView(generic.ListView):
    template_name = 'teacher/communication.html'

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
                    return HttpResponse("<h1>you are logged in as teacher</h1>"+user.email)
                except:
                    try:
                        parent = user.parent
                        return HttpResponse("<h1>you are logged in as parent</h1>"+user.parent.studentID.surname)
                    except:
                        try:
                            administrativeOfficer = user.administrativeofficer
                            return HttpResponse("<h1>you are logged in as Adminstrative officer</h1>")
                        except:
                            try:
                                principle = user.principle
                                return HttpResponse("<h1>you are logged in as principle</h1>")
                            except:
                                return HttpResponse("<h1>you are logged in with stuped account </h1>")
                #return HttpResponse("<h1>you are logged in </h1>")
        else:
            return render(request, 'application/login.html', {'error_message': 'Invalid login'})
    return render(request, 'application/login.html')
