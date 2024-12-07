from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from clubs.models import Club


class Competitions(models.Model):
    title = models.CharField(
        max_length=100,
    )
    date = models.DateField(

    )
    context = models.TextField(

    )

    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="competitions"
    )

    participants = models.ManyToManyField(
        User,
        related_name='joined_participants',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - Hosted by {self.club.title} on {self.date}"
