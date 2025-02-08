from rest_framework import serializers
from .models import CustomUser  # Import CustomUser instead of User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  # Use CustomUser here
        fields = ['username', 'name', 'password']

    def create(self, validated_data):
        user = CustomUser(  # Use CustomUser here
            username=validated_data['username'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user