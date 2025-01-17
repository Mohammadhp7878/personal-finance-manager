from django.contrib import admin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "phone"]
    list_per_page = 10
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user__id", "first_name", "last_name", "user__phone", "is_profile_completed"]
    list_per_page = 10
    # list_editable
    
    def is_profile_completed(self, obj):
        if obj.first_name and obj.last_name and obj.email:
            return "True"
        else: 
            return "False"
         