from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skin_type', 'age', 'location', 'created_at')
    list_filter = ('skin_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')
