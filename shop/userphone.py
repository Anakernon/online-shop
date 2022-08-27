from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = forms.CharField(max_length = 13, required = True, default = "+380000000000")
