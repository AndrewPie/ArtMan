import os
from django.conf import settings
from django import template

from cargo_spec.models import Specification

register = template.Library()

@register.filter
def check_scan_file(marking):
    scan_dir = f'{settings.BASE_DIR}/media/cargo_spec/{marking}/scan'
    if os.path.exists(scan_dir) and os.path.isdir(scan_dir):
        if not os.listdir(scan_dir):
            return False
        else:    
            return True
    else:
        return False
    
    
@register.filter
def sort_docs(query):
    return sorted(query, key=lambda x: os.path.basename(x.document.name), reverse=True)