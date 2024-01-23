from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.conf import settings

from accounts.models import UserLoginSessionInfo
from django.core.cache import cache

# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def home(request):
    # device_name = get_device_name_from_request(request)
    # session_data = request.session
    # Iterate through the session data
    # for key, value in session_data.items():
        # print(f"{key}: {value}")

    # session_id = request.session.session_key

    # Do something with the session ID
    # print("Session ID:", session_id)
    return render(request, 'core/home.html')

def account(request):
    deviced_loggedin = UserLoginSessionInfo.objects.filter(user=request.user)
    session_key = request.session.session_key

    for device in deviced_loggedin:
        if device.session_key == session_key:
            device_id = device.device_id

    context = {
        'deviced_loggedin' : deviced_loggedin,
        'device_id' : device_id,
    }
    return render(request, 'core/account.html', context)

def logout_device(request, device_id):
    user = request.user
    UserLoginSessionInfo.objects.filter(device_id=device_id, user=user).delete()
    return redirect('account')