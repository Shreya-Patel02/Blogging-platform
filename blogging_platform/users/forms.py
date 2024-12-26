from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    role_choices = User.ROLES[1:]  # Exclude 'Owner' for the form
    role = forms.ChoiceField(choices=role_choices, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


