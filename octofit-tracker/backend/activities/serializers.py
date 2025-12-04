from rest_framework import serializers
from activities.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for Activity model
    """
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id',
            'user_id',
            'username',
            'activity_type',
            'title',
            'description',
            'duration_minutes',
            'calories_burned',
            'distance_km',
            'intensity',
            'date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at']
