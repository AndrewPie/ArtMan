from django import forms

from report.models import Report, Section, Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title']
        labels = {'title': 'Wpis'}