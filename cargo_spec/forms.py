from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .models import Specification, CargoContent

class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        exclude = ['marking', 'owner', 'capacity', 'approved']
        labels = {
            'package_type': 'Rodzaj opakowania',
            'dimension_length': 'Wymiar w cm [dł]',
            'dimension_width': 'Wymiar w cm [szer]',
            'dimension_height': 'Wymiar w cm [wys]',
            'weight': 'Waga w kg',
            'storage': 'Warunki przechowywania',
            'description': 'Opis',
            'total_value': 'Łączna wartość'
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

CargoContentFormSet = inlineformset_factory(Specification, CargoContent, form=CargoContentForm, extra=0, min_num=1, validate_min=True, max_num=20, validate_max=True, can_delete=True)