from django.contrib import admin

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

