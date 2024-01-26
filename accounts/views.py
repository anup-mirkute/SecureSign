import os
import mimetypes
from django.shortcuts import render, redirect, reverse

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .forms import LoginForm, SignupForm, EmailInputForm, PasswordResetForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from django.conf import settings

from django.views.decorators.csrf import csrf_protect

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils import timezone

from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.template.loader import render_to_string

from datetime import timedelta


def generate_token(request, user, path_name):
    generate_token = default_token_generator
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token.make_token(user)
    url = request.build_absolute_uri(reverse(path_name, kwargs={'uidb64' : uid, 'token' : token}))
    return url

class EmailSender:
    '''
    subject         ->  str     :   Mandatory : Subject of the Mail
    recipient_list  ->  list    :   List of mail addresses that you want to send the mail
    user            ->  str     :   current user's username 
    message         ->  str     :   A message is optional if you want to send the template with the mail otherwise it is mandatory field and having with HTML attribute.
    cc_email        ->  list    :   List of mail addresses that you want to keep in cc
    bcc_email       ->  list    :   List of mail addresses that you want to keep in bcc
    template_name   ->  str     :   A template_name is optional if you just want to send a message with the mail otherwise it is mandatory field to send the template with the mail.
    links           ->  list    :   Optional : A Link with the mail
    otp             ->  str     :   Optional : A OTP with the mail
    token           ->  str     :   Optional : A token with the mail

    '''
    def __init__(self, subject, recipient_list, user=None, message=None, cc_email=None, bcc_email=None, template_name=None, file_name=None, links=None, otp=None, token=None):
        self.subject = subject
        self.from_mail = settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        self.user = user
        self.message = message
        self.cc_email = cc_email
        self.bcc_email = bcc_email
        self.template_name = template_name
        self.file_name = file_name
        self.links = links
        self.otp = otp
        self.token = token

    def sending_mail(self):
        if self.template_name is not None:
            template = 'email_template/' + self.template_name
            context = {
                'user' : self.user,
                'recipient_list' : self.recipient_list,
                'links' : self.links,
                'otp' : self.otp,
                'token' : self.token,
            }
            html_content = render_to_string(template, context)
        else:
            html_content = self.message

        text_content = strip_tags(html_content) 
        msg = EmailMultiAlternatives(self.subject, text_content, self.from_mail, self.recipient_list)
        msg.attach_alternative(html_content, "text/html")

        if self.cc_email is not None:
            msg.cc = self.cc_email

        if self.bcc_email is not None:
            msg.bcc = self.bcc_email

        if self.file_name is not None:
            file_path = os.path.join(settings.MEDIA_ROOT, 'email_attachment', self.file_name)

            # Determine the content type and encoding for the attachment
            content_type, encoding = mimetypes.guess_type(file_path)
            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'  # Default content type if it cannot be determined

            with open(file_path, 'rb') as file:
                msg.attach(self.file_name, file.read(), content_type)


        msg.send()

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Username does not exists')
                return redirect('login')
            
            if user.is_active:
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user is not None:
                    loginUser(request, authenticated_user)
                    request.session['username'] = username
                    request.session['email']    = user.email
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request, 'Incorrect Credentials')
                    return redirect('login')
            else :
                messages.error(request, 'Please verify your email address')
                return redirect('login')
            
    form = LoginForm
    context = {'form' : form,}
    return render(request, 'accounts/login.html', context)

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            email = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password'].strip()

            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists! Try logging in.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            else:
                # Save the user object but set is_active status False
                user = User(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                # Sending the verification mail to user 
                reset_url = generate_token(request, user, 'verify-mail')
                subject = 'Email Confirmation'
                page = 'email_verification_mail.html'
                # sendingMail(page, subject, reset_url, email, username)
                mail = EmailSender(subject, [email], user=username, template_name=page, token=reset_url)
                mail.sending_mail()

                messages.success(request, 'Account created!! Please verify your email')
                return redirect('send-verification-mail', user)
    form = SignupForm
    context = {'form' : form}
    return render(request, 'accounts/signup.html', context)


@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    request.session.clear()
    logoutUser(request)
    request.session['website_name'] = settings.WEBSITE_NAME
    return redirect('login')

@csrf_protect
def verifyMail(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            limit_date = user.date_joined + timedelta(days=1)
            print(limit_date)
            if limit_date >= timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, 'Email verify successfully')
                return redirect('login')
            else:
                messages.error(request, 'Verification link is expired. Rejoin us')
                return redirect('signup')
        else:
            messages.error(request, 'User is already verified')
            return redirect('login')
    else:
        messages.error(request, 'Verification link is invalid')
        return redirect('signup')

@csrf_protect 
def sendVerificationMail(request, user):
    try:
        get_user = User.objects.get(username=user)
    except User.DoesNotExist:
        messages.error(request, 'User Does not exists')
        return redirect('login')

    if not get_user.is_active:
        if request.method == 'POST':
            # Resend the verification mail to the user
            reset_url = generate_token(request, get_user, 'verify-mail')
            subject = 'Email Confirmation'
            page = 'email_verification_mail.html'
            # sendingMail(page, subject, reset_url, get_user.email, get_user)
            mail = EmailSender(subject, [get_user.email], user=get_user, template_name=page, token=reset_url)
            mail.sending_mail()

            messages.success(request, 'Verification link has been send to your mail')
    else:
        return HttpResponseRedirect(reverse('login'))
    
    context = {'user' : user}
    return render(request, 'accounts/send-verification-mail.html', context)

@csrf_protect
def sendPasswordResetMail(request):
    if request.method == 'POST':
        form = EmailInputForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    messages.error(request, 'Unverified email address')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Email does not exists.')
                return redirect('send-password-reset-mail')
            
            if user:
                # Sending mail to user
                reset_url = generate_token(request, user, 'reset-password')
                subject = 'Passsword reset for your account'
                page = 'forget_password_mail.html'
                # sendingMail(page, subject, reset_url, user.email, user.username)
                mail = EmailSender(subject, [user.email], user=user, template_name=page, token=reset_url)
                mail.sending_mail()

                messages.success(request, 'Password reset link has been sent to your mail')
                return redirect('login')
    else:
        form = EmailInputForm
        context = {'form' : form}
    return render(request, 'accounts/send-password-reset-mail.html', context)

@csrf_protect
def resetPassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None

    if not user.is_active:
        messages.error(request, 'Unverified email address')
        return redirect('login')

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password'].strip()
                repassword = form.cleaned_data['repassword'].strip()
                if password == repassword:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successfully. Login now')
                    return HttpResponseRedirect(reverse('login'))
        form = PasswordResetForm
        context = {'form' : form}
        return render(request, 'accounts/reset-password.html', context)
    else:
        messages.error(request, 'The reset password link is invalid.')
        return HttpResponseRedirect(reverse('send-password-reset-mail'))


def isUsernameExist(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.POST.get('username', None)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'valid':'False', 'message':'Username already exists'})
        else:
            return JsonResponse({'valid':'True', 'message':'Username Found'})
    else :
        pass