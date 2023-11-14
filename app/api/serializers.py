import re

from rest_framework import serializers

from api.models import CadastralNumber

class CadastralNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralNumber
        fields = ['number', 'long', 'alt']
        
    def validate_number(self, value):
        """Check if number has acceptable format"""
        if re.fullmatch(r"^\d{2}:\d{2}:\d{7}:\d{2}$", value):
            return value
        raise serializers.ValidationError("The number must be in format - '23:34:1234567:12'")
    
    def validate_long(self, value):
        """Check if alt or long has acceptable format"""
        if re.fullmatch(r"^\d{1,3}.\d{5}$", value):
            return value
        raise serializers.ValidationError("The alt/long must be in format - '41.40338'")
    
    def validate_alt(self, value):
        """Check if alt or long has acceptable format"""
        if re.fullmatch(r"^\d{1,3}.\d{5}$", value):
            return value
        raise serializers.ValidationError("The alt/long must be in format - '41.40338'")
    