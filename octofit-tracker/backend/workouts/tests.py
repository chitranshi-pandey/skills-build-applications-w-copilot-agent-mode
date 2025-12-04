from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from workouts.models import WorkoutPlan, WorkoutSession

User = get_user_model()


class WorkoutPlanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.plan = WorkoutPlan.objects.create(
            user=self.user,
            title='Weight Loss Program',
            goal='weight_loss',
            difficulty_level='beginner',
            duration_weeks=12,
            workouts_per_week=3
        )

    def test_workout_plan_creation(self):
        self.assertEqual(self.plan.title, 'Weight Loss Program')
        self.assertEqual(self.plan.goal, 'weight_loss')
        self.assertEqual(self.plan.user, self.user)

    def test_workout_plan_string_representation(self):
        expected = f"{self.user.username} - Weight Loss Program"
        self.assertEqual(str(self.plan), expected)


class WorkoutPlanViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_workout_plan(self):
        data = {
            'title': 'New Workout Plan',
            'goal': 'muscle_gain',
            'difficulty_level': 'intermediate',
            'duration_weeks': 8,
            'workouts_per_week': 4
        }
        response = self.client.post('/api/workout-plans/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutPlan.objects.count(), 1)

    def test_list_user_workout_plans(self):
        WorkoutPlan.objects.create(
            user=self.user,
            title='Test Plan',
            goal='muscle_gain',
            difficulty_level='beginner',
            duration_weeks=12,
            workouts_per_week=3
        )
        response = self.client.get('/api/workout-plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

