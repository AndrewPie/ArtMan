from django.contrib import admin

from .models import Specification,SpecificationDocument, CargoContent,SpecificationDocumentsExcel

admin.site.register(Specification)
admin.site.register(CargoContent)
admin.site.register(SpecificationDocumentsExcel)
admin.site.register(SpecificationDocument)

