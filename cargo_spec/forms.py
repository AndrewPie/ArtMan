from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .models import Specification, CargoContent, SpecificationDocument

class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        exclude = ['marking', 'owner', 'capacity', 'approved']
        widgets = {
            'total_value': forms.NumberInput(attrs={'readonly': True}),
        }
        labels = {
            'package_type': 'Rodzaj opakowania',
            'dimension_length': 'Długość [cm]',
            'dimension_width': 'Szerokość [cm]',
            'dimension_height': 'Wysokość [cm]',
            'weight': 'Waga [kg]',
            'storage': 'Warunki przechowywania',
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

CargoContentFormSet = inlineformset_factory(Specification, CargoContent, form=CargoContentForm, extra=0, min_num=1, validate_min=True, max_num=20, validate_max=True, can_delete=True)


class SpecificationDocumentForm(forms.ModelForm):
    file_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = SpecificationDocument
        fields = ['description', 'document']