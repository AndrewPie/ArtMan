from django import forms

from report.models import Report, Section, Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title']
        labels = {'title': 'Wpis'}
        

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = ['section_master', 'report']
        labels = {
            'title': 'Nazwa',
            'text_entry': 'Tekst początkowy',
            'text_end': 'Tekst końcowy',
        }