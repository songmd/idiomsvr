from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Idioms)
class IdiomsAdmin(admin.ModelAdmin):
    pass
