from rest_framework import serializers
from .models import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'total', 'items']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_status(self, value):
        if self.instance and self.instance.status == 'CANCELLED' and value != 'CANCELLED':
            raise serializers.ValidationError("Cannot change status of a cancelled order.")
        return value
