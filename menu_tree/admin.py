from django.contrib import admin
from .models import MenuItem

# Register your models here.

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent', 'menu_name', 'order']
    list_filter = ['menu_name']
    search_fields = ['name', 'menu_name']