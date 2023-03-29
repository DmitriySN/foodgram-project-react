from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    empty_value_display = '-пусто-'
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'date_joined',
        'password',
    )
