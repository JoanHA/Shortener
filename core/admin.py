from django.contrib import admin
from .models import Link 

# Register your models here.

@admin.register(Link)

class Admin(admin.ModelAdmin):
    pass    
