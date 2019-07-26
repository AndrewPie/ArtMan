from django.contrib import admin

from .models import Specification, CargoContent, SpecificationDocument

admin.site.register(Specification)
admin.site.register(CargoContent)
admin.site.register(SpecificationDocument)