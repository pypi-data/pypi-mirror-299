from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
    ]
    list_display = [
        'user',
        'authenticated_at',
    ]
    autocomplete_fields = ['user']

