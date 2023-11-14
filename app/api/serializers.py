import re

from rest_framework import serializers

from api.models import CadastralNumber, History

def number_validator(value):
    if re.fullmatch(r"^\d{2}:\d{2}:\d{7}:\d{2}$", value):
        return value
    return None

def long_alt_validator(value):
    if re.fullmatch(r"^\d{1,3}.\d{5}$", value):
            return value
    return None

class CadastralNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastralNumber
        fields = ['number', 'long', 'alt', 'status']
        
    def to_representation(self, instance):
        """Convert `status` to appropriate value."""
        ret = super().to_representation(instance)
        if ret['status'] is None:
            ret['status'] = 'Data is still processing, try later'
        return ret
    
    def validate_number(self, value):
        """Check if number has acceptable format"""
        if number_validator(value):
            return value
        raise serializers.ValidationError(
            "The number must be in format - '23:34:1234567:12'"
        )
    
    def validate_long(self, value):
        """Check if alt or long has acceptable format"""
        if long_alt_validator(value):
            return value
        raise serializers.ValidationError(
            "The alt/long must be in format - '41.40338'"
        )
    
    def validate_alt(self, value):
        """Check if alt or long has acceptable format"""
        if long_alt_validator(value):
            return value
        raise serializers.ValidationError(
            "The alt/long must be in format - '41.40338'"
        )

class CadastralNumberResultSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=16)
    
    def validate_number(self, value):
        if number_validator(value):
            return value
        raise serializers.ValidationError(
            "The number must be in format - '23:34:1234567:12'"
        )

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['request_type', 'timestamp']
        
class CadastralHistorySerializer(serializers.ModelSerializer):
    history_set = HistorySerializer(many=True, read_only=True)
    class Meta:
        model = CadastralNumber
        fields = ['number', 'long', 'alt', 'status', 'history_set']

        
