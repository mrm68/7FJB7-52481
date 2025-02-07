from rest_framework import serializers
from .models import Reservation
class Reservation_Serializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        fields = (
            'id',
            "username",
            "seats_reserved",
            "cost",
        )
        read_only_fields = ['cost']
        model = Reservation