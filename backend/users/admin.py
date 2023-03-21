from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display = ('username', 'email', 'id')
