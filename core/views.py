from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.conf import settings

# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def home(request):
    return render(request, 'core/home.html')