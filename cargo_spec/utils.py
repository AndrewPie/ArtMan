from datetime import datetime

from .models import Specification

def specification_marking(self):
    mark = f'{datetime.now().year}-{self.instance.owner.first_name[0]}{self.instance.owner.last_name[0]}-{self.instance.package_type[:2].upper()}'
    query = Specification.objects.filter(marking__icontains=mark)
    return f'{mark}-{len(query)+1}'