import re
from rest_framework import serializers

class CustomUserSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{10,14}$', value):
            raise serializers.ValidationError("Invalid phone number format.")
        
        return value
        