from django.contrib import admin
# from .models import Workers
# Register your models here.
# admin.site.register(Workers)
from .models import User

admin.site.register([User,])