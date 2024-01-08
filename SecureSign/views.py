from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def index(request):
    request.session['website_name'] = settings.WEBSITE_NAME
    return render(request, 'index.html')