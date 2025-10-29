from django.contrib import admin
from .models import CustomUser
from doctor.models import Doctor

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Doctor)

