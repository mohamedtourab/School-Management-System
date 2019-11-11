from django.contrib.auth import authenticate, login
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

    #             albums = Album.objects.filter(user=request.user)
    #             return render(request, 'music/index.html', {'albums': albums})
    #         else:
    #             return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'application/login.html', {'error_message': 'Invalid login'})
    return render(request, 'application/login.html')
