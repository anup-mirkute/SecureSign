from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from .models import UserLoginSessionInfo
from django.dispatch import receiver
from datetime import datetime


def create_device_id(user):
    now = datetime.now()
    device_id = str(user) + str(now.strftime("%d%m%Y%H%M%S"))
    return device_id

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in, sender=User)
def user_login_session(sender, request, user, **kwargs):
    device_id = create_device_id(user.id)
    session_key = request.session.session_key
    ip_address = get_client_ip(request)

    is_mobile = request.user_agent.is_mobile
    is_tablet = request.user_agent.is_tablet 
    is_touch_capable = request.user_agent.is_touch_capable
    is_pc = request.user_agent.is_pc 
    is_bot = request.user_agent.is_bot 

    # Accessing user agent's browser attributes
    user_browser_family = request.user_agent.browser.family
    user_browser_version = request.user_agent.browser.version
    user_browser_version_string = request.user_agent.browser.version_string

    # Operating System properties
    user_os_family = request.user_agent.os.family
    user_os_version = request.user_agent.os.version 
    user_os_version_string = request.user_agent.os.version_string 

    # Device properties
    user_device_family = request.user_agent.device.family
    
    UserLoginSessionInfo.objects.create(
        user=user, session_key=session_key, device_id=device_id, ip_address=ip_address,
        is_mobile=is_mobile, is_tablet=is_tablet, is_touch_capable=is_touch_capable, is_pc=is_pc, is_bot=is_bot,
        user_browser_family=user_browser_family, user_browser_version=user_browser_version, user_browser_version_string=user_browser_version_string,
        user_os_family=user_os_family, user_os_version=user_os_version, user_os_version_string=user_os_version_string,
        user_device_family=user_device_family
    )

# user_logged_in.connect(user_login_session, sender=User)
    
@receiver(user_logged_out, sender=User)
def user_logout_session(sender, request, user, **kwargs):
    # if cache.get('device_id'):
    #     device_id = cache.get('device_id')
    #     UserLoginSessionInfo.objects.filter(device_id=device_id, user=user).delete()
    # else:
    #     pass
    try :
        session_key = request.session.session_key
        UserLoginSessionInfo.objects.filter(session_key=session_key, user=user).delete()
    except Exception as e:
        print(e)