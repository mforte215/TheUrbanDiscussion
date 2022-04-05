from audioop import reverse
import re
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
def IndexView(request):
    return render(request, 'app/index.html')

def LoginView(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'registration/login.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            context = {'error_message', 'Sorry, Username/Password Not Found'}
            return render(request, 'registration/login.html', context)
    

class SignUpForm(generic.CreateView):
    form_class= UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"