from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Activity(models.Model):
    """
    Model to track user activities
    """
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    calories_burned = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    distance_km = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
        ],
        default='moderate'
    )
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.date.date()})"
