from datetime import datetime

from .models import Specification

def specification_marking(self):
    mark = f'{datetime.now().year}-{self.instance.owner.first_name[0]}{self.instance.owner.last_name[0]}-{self.instance.package_type[:2].upper()}'
    
    query_list = Specification.objects.filter(marking__contains=mark).values_list('marking', flat=True)
    
    try:
        val_list = [int(i[11:]) for i in query_list]
        number = min(set(range(1, len(query_list) + 1)) - set(val_list))
    except Exception:
        number = len(query_list) + 1
    
    return f'{mark}-{number}'