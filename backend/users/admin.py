from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    list_display_links = ('email', 'username')
    list_filter = ('email', 'username')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ['email', 'first_name', 'last_name']}),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
