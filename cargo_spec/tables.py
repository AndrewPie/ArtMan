import django_tables2 as tables

from cargo_spec.models import CargoContent


class CargoContentTable(tables.Table):
    ordinal_number = tables.Column(verbose_name='lp.')
    
    class Meta:
        model = CargoContent
        fields = ['ordinal_number', 'name', 'serial_number', 'quantity', 'unit_of_measurement', 'value']
        orderable = False
        attrs = {
            'thead': {
                'class': 'thead-light'
            }
        }