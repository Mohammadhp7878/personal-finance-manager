import re
from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{10,14}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        
        return value
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email", ]
        