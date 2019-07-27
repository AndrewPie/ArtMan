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
        fields = ['section_master', 'title', 'text_entry', 'text_end']
        labels = {
            'title': 'Nazwa',
            'text_entry': 'Tekst początkowy',
            'text_end': 'Tekst końcowy',
            'section_master': 'Sekcja główna'
        }