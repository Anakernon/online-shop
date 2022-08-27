from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Info


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length = 13, required = True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]
        
class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ["name", "text"]

class ProfileSettingsForm(forms.Form):
    username = forms.CharField(max_length = 64, required = False)
    first_name = forms.CharField(max_length = 32, required = False, label='Your name')
    last_name = forms.CharField(max_length = 32, required = False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length = 13, required = False)
    password = forms.CharField(widget=forms.PasswordInput(), required = False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required = False)
    address = forms.CharField(max_length = 128, required = False)
    
    def clean(self):
        cleaned_data = super(ProfileSettingsForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        
        
        
        
        
        
        
        
        
        
        
        
    

