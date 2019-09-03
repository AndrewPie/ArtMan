import os
from datetime import datetime
from django.conf import settings

from cargo_spec.models import Specification

def specification_marking(self):
    mark = f'{datetime.now().year}-{self.instance.owner.first_name[0]}{self.instance.owner.last_name[0]}-{self.instance.package_type[:2].upper()}'
    
    query_list = Specification.objects.filter(marking__contains=mark).values_list('marking', flat=True)
    
    try:
        val_list = [int(i[11:]) for i in query_list]
        number = min(set(range(1, len(query_list) + 1)) - set(val_list))
    except Exception:
        number = len(query_list) + 1
    
    return f'{mark}-{number}'


def check_scan_file(marking):
    scan_dir = f'{settings.BASE_DIR}/media/cargo_spec/{marking}/scan'
    if os.path.exists(scan_dir) and os.path.isdir(scan_dir):
        if not os.listdir(scan_dir):
            return False
        else:    
            return True
    else:
        return False
