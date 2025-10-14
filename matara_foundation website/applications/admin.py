from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'county', 'status', 'created_at')
    list_filter = ('status', 'county')
    search_fields = ('full_name', 'email', 'phone_number')
