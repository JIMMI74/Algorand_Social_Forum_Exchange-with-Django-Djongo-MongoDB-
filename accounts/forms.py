from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.CharField(max_length=50, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username',  'email', 'password',)



