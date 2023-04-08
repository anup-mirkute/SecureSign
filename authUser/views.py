from django.shortcuts import render
from django.http import HttpResponse
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.get(username=username)
            

    form = LoginForm
    context = {
        'form' : form,
    }
    return render(request, 'auth/login.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return HttpResponse(user)

    form = SignupForm
    context ={
        'form': form,
    }
    return render(request, 'auth/signup.html', context)