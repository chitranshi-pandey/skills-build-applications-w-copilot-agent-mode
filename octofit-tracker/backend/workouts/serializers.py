from rest_framework import serializers
from workouts.models import WorkoutPlan, WorkoutSession


class WorkoutSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkoutSession model
    """
    class Meta:
        model = WorkoutSession
        fields = [
            'id',
            'workout_plan',
            'day_number',
            'title',
            'description',
            'duration_minutes',
            'exercises',
            'is_completed',
            'completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkoutPlan model
    """
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    sessions = WorkoutSessionSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'id',
            'user_id',
            'username',
            'title',
            'description',
            'goal',
            'difficulty_level',
            'duration_weeks',
            'workouts_per_week',
            'is_active',
            'sessions',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at']
