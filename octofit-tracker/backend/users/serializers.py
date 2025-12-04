from rest_framework import serializers
from users.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'profile_image',
            'fitness_level',
            'location',
            'date_joined',
            'updated_at',
        ]
        read_only_fields = ['id', 'date_joined', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'goals',
            'target_steps_per_day',
            'target_calories_per_day',
            'preferences',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
