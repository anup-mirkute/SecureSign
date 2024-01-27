from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def index(request):
    brand = settings.WEBSITE_NAME
    context = {
        'brand' : brand,
    }
    return render(request, 'index.html', context)