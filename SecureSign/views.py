from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def website_name(request):
    brand = settings.WEBSITE_NAME
    return {'brand': brand}

def index(request):
    return render(request, 'index.html')