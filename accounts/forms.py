from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#         widgets = {'password': PasswordInput()}

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({
#             'class' : 'form-control form-control-lg',
#             'placeholder' : 'Username',
#             'id' : 'username',
#         })
#         self.fields['email'].widget.attrs.update({
#             'class' : 'form-control form-control-lg',
#             'placeholder' : 'Email address',
#             'id' : 'email',
#         })
#         self.fields['password'].widget.attrs.update({
#             'class' : 'form-control form-control-lg',
#             'placeholder' : 'Password',
#             'id' : 'password',
#         })
class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Username',
        'id' : 'username',
        'spellcheck' : 'false',
    }))
    email = forms.CharField(label='Email Address', max_length=320, widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email Address',
        'id' : 'email', 
    }))
    password = forms.CharField(label='Password', max_length=15, widget=forms.PasswordInput(attrs={
        'class' : 'form-control form-control-lg',
        'placeholder' : 'Password',
        'id' : 'password',
    }))

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Username',
        'id' : 'username',
        'spellcheck' : 'false', 
    }))
    password = forms.CharField(label='Password', max_length=15, widget=forms.PasswordInput(attrs={
        'class' : 'form-control form-control-lg',
        'placeholder' : 'Password',
        'id' : 'password',
    }))

class EmailInputForm(forms.Form):
    email = forms.CharField(label='Email Address', max_length=320, widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email Address',
        'id' : 'email', 
    }))

class PasswordResetForm(forms.Form):
    password = forms.CharField(label='Password', max_length=15, widget=forms.PasswordInput(attrs={
        'class' : 'form-control form-control-lg',
        'placeholder' : 'Password',
        'id' : 'password',
    }))
    repassword = forms.CharField(label='Confirm Password', max_length=15, widget=forms.PasswordInput(attrs={
        'class' : 'form-control form-control-lg',
        'placeholder' : 'Confirm password',
        'id' : 'repassword',
    }))