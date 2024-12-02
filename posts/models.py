from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models, IntegrityError

class Post(models.Model):
    class Meta:
        verbose_name = "Post"

    title = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(5),
        ]
    )

    image_url = models.URLField()

    content = models.TextField()

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
        related_name='posts',
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
