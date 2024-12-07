from django.db import models
from django.utils.text import slugify
from users.models import Users
from django.contrib.auth.models import User

class Club(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
    )
    image = models.URLField(
    )
    content = models.TextField(
    )
    owner = models.CharField(
        max_length=100,
    )
    members = models.ManyToManyField(
        User,
        related_name='joined_clubs',
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    uploaded_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    user = models.ForeignKey(
        to='users.Users',
        on_delete=models.CASCADE,
        related_name='clubs',
        editable=False,
    )

    def short_content(self):
        return self.content[:50] + '...' if len(self.content) > 50 else self.content

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title