from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .models import Specification, CargoContent, SpecificationDocument

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        exclude = ['marking', 'owner', 'capacity', 'approved']
        widgets = {
            'total_value': forms.NumberInput(attrs={'readonly': True}),
        }
        labels = {
            'package_type': 'Rodzaj opakowania',
            'storage': 'Warunki przechowywania',
            'dimension_length': 'Długość [cm]',
            'dimension_width': 'Szerokość [cm]',
            'dimension_height': 'Wysokość [cm]',
            'weight': 'Waga [kg]',
            'description': 'Opis',
            'total_value': 'Łączna wartość (PLN)'
        }
        error_messages = {
            'dimension_length': {'min_value': "Wartość musi być conajmniej równa 1"},
            'dimension_width': {'min_value': "Wartość musi być conajmniej równa 1"},
            'dimension_height': {'min_value': "Wartość musi być conajmniej równa 1"}
        }
                    
    
class CargoContentForm(forms.ModelForm):
    class Meta:
        model = CargoContent
        exclude = ['specification']
        labels = {
            'name': 'nazwa',
            'serial_number': 'nr seryjny**',
            'quantity': 'ilość',
            'unit_of_measurement': 'jedn. miary',
            'value': 'wartość (PLN)'
        }
        
    def __init__(self, *args, **kwargs):
        super(CargoContentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': f'Pole "{field.label.capitalize()}" jest wymagane'}
        # usuwa labels dla każdego pola (w tym przypadku dla każdej linii CargoContent)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        
        # usuwa label tylko z konkretnego pola
        # self.fields['name'].label = False
        
        
CargoContentFormSet = inlineformset_factory(Specification, CargoContent, form=CargoContentForm, extra=0, min_num=1, validate_min=True, max_num=20, validate_max=True, can_delete=True)


class SingleSpecificationDocumentForm(forms.ModelForm):
    file_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = SpecificationDocument
        fields = ['description', 'document']
        labels = {
            'description': 'Opis',
            'document': 'Plik'
        }
        error_messages = {
            'document': {'required': 'Należy wybrać plik'},
        }


class MultipleSpecificationDocumentForm(forms.Form):
    description = forms.CharField(max_length=255, required=False, label='Opis')
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Plik/Pliki', error_messages={'required': 'Należy wybrać plik/pliki'})