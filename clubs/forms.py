from django import forms

from SoftUniFinalExam.mixins import ReadOnlyMixin, PlaceholderMixin
from clubs.models import Club


class ClubBaseForm(forms.ModelForm):
    class Meta:
        model = Club
        exclude = ('users', 'slug', 'members')

class ClubCreateForm(ClubBaseForm):
    pass

class ClubEditForm(PlaceholderMixin,ClubBaseForm):
    pass

class ClubDeleteForm(ReadOnlyMixin, ClubBaseForm):
    readonly_fields = ['title','image', 'owner' 'content']