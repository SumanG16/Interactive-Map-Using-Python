from django.contrib import admin

# Register your models here.
# map_app/admin.py
from django.contrib import admin
from .models import Location  # Ensure the correct import path

# Register your model with the admin site
admin.site.register(Location)



