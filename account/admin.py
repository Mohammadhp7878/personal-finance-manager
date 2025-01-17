from django.contrib import admin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    ...
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    ...