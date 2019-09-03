import itertools

import django_tables2 as tables

from cargo_spec.models import CargoContent


class CargoContentTable(tables.Table):
    ordinal_number = tables.Column(empty_values=(), verbose_name='lp.')
    
    def __init__(self, *args, **kwargs):
        super(CargoContentTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count(1)
        
    def render_ordinal_number(self):
        return f'{next(self.counter)}'
    
    class Meta:
        model = CargoContent
        fields = ['ordinal_number', 'name', 'serial_number', 'quantity', 'unit_of_measurement', 'value']
        orderable = False
        attrs = {
            'thead': {
                'class': 'thead-light'
            }
        }
