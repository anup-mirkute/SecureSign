from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings 
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserLoginSessionInfo

class AppAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # Check if the requested URL belongs to the specified app
        # if any(request.path.startswith(f'/{app_name}/') for app_name in settings.APPS_TO_RESTRICT) and not request.user.is_authenticated:
        #     # Redirect to the login page if the user is not authenticated
        #     return redirect(reverse('login'))
        
        # if any(request.path.startswith(f'/{app_name}/') for app_name in settings.APPS_TO_RESTRICT) and request.user.is_authenticated:
        #     session_id = request.session.session_key
        #     try:
        #         user = UserLoginSessionInfo.objects.get(session_key=session_id)
        #     except UserLoginSessionInfo.DoesNotExist:
        #         # Redirect to the login page if the session key is not found
        #         print("UserLoginSessionInfo not found for session key:", session_id)
        #         # return render(request, 'accounts/login.html')
        #         return redirect(reverse('logout'))
        #     except Exception as e:
        #         # Handle other exceptions
        #         print(e)
        #         return redirect(reverse('logout'))
            
        if any(request.path.startswith(f'/{app_name}/') for app_name in settings.APPS_TO_RESTRICT):

            if not request.user.is_authenticated:
                return redirect(reverse('login'))
            
            session_id = request.session.session_key
            # if not UserLoginSessionInfo.objects.filter(session_key=session_id).exists():
            #     return redirect(reverse('logout'))
            
            try:
                user = UserLoginSessionInfo.objects.get(session_key=session_id)
            except UserLoginSessionInfo.DoesNotExist:
                # Redirect to the login page if the session key is not found
                print("UserLoginSessionInfo not found for session key:", session_id)
                # return render(request, 'accounts/login.html')
                return redirect(reverse('logout'))
            except Exception as e:
                # Handle other exceptions
                print(e)
                return redirect(reverse('logout'))
        
        response = self.get_response(request)
        return response