import re
from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{10,14}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        
        return value

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["phone", "id"]    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email", "user"]
        extra_kwargs = {
            "user": {"read_only": True}
        }
        