from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class' :   'form-control',
            'id'    :   'username',
            'placeholder'   :   'Enter username',
        })
        self.fields['email'].widget.attrs.update({
            'class' :   'form-control',
            'id'    :   'email',
            'placeholder'   :   'Enter email address',
        })
        self.fields['password'].widget.attrs.update({
            'class' :   'form-control',
            'id'    :   'password',
            'placeholder'   :   'Enter password',
        })

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25, widget=forms.TextInput(attrs={
        'class' :   'form-control',
        'id'    :   'username',
        'placeholder'   :   'Enter username',
    }))
    password = forms.CharField(label='Password', max_length=15, widget=forms.PasswordInput(attrs={
        'class' :   'form-control',
        'id'    :   'password',
        'placeholder'   :   'Enter password',
    }))