from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length = 13, required = True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]
        
class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = Patch
        fields = ["name", "text"]
