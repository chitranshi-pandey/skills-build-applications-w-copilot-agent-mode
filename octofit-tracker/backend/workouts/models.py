from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class WorkoutPlan(models.Model):
    """
    Model for personalized workout plans
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    goal = models.CharField(
        max_length=50,
        choices=[
            ('weight_loss', 'Weight Loss'),
            ('muscle_gain', 'Muscle Gain'),
            ('endurance', 'Endurance'),
            ('flexibility', 'Flexibility'),
            ('general_fitness', 'General Fitness'),
        ]
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    duration_weeks = models.IntegerField(validators=[MinValueValidator(1)])
    workouts_per_week = models.IntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workout_plans'

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class WorkoutSession(models.Model):
    """
    Model for individual workout sessions
    """
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='sessions')
    day_number = models.IntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    exercises = models.JSONField(default=list, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workout_sessions'

    def __str__(self):
        return f"{self.workout_plan.title} - Day {self.day_number}"
