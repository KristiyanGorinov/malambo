from django import forms

from SoftUniFinalExam.mixins import ReadOnlyMixin, PlaceholderMixin
from competitions.models import Competitions


class CompetitionBaseForm(forms.ModelForm):
    class Meta:
        model = Competitions
        exclude = ('slug', 'participants')

class CompetitionCreateForm(CompetitionBaseForm):
    pass

class CompetitionEditForm(PlaceholderMixin,CompetitionBaseForm):
    pass

class CompetitionDeleteForm(ReadOnlyMixin, CompetitionBaseForm):
    readonly_fields = ['title', 'club', 'context', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.readonly_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.readonly_fields:
            if field_name in cleaned_data and self.instance:
                cleaned_data[field_name] = getattr(self.instance, field_name)
        return cleaned_data