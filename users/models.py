from django.core.validators import MinLengthValidator
from django.db import models
from users.validators import IsAlphaValidator
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=50)
    info = models.TextField(null=False, blank=False,)
    date_created = models.DateTimeField(auto_now_add=True)

