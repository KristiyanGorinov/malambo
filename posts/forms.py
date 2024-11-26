from django import forms

from SoftUniFinalExam.mixins import ReadOnlyMixin
from posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('users',)

class PostCreateForm(PostBaseForm):
    pass

class PostsEditForm(PostBaseForm):
    pass

class PostDeleteForm(ReadOnlyMixin, PostBaseForm):
    readonly_fields = ['title', 'image_url', 'content']
