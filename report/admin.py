from django.contrib import admin

from report.models import Report, Section, Note

admin.site.register(Report)
admin.site.register(Section)
admin.site.register(Note)