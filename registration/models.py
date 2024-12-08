from django.contrib.auth.models import User
from django.db import models

from competitions.models import Competitions
from users.models import Users


class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE, related_name="registrations")

