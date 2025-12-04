from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from activities.models import Activity

User = get_user_model()


class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Morning Run',
            duration_minutes=30,
            calories_burned=300,
            distance_km=5.0,
            intensity='moderate',
            date=timezone.now()
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.title, 'Morning Run')
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.user, self.user)

    def test_activity_string_representation(self):
        expected = f"{self.user.username} - Morning Run ({self.activity.date.date()})"
        self.assertEqual(str(self.activity), expected)


class ActivityViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_activity(self):
        data = {
            'activity_type': 'running',
            'title': 'Morning Run',
            'duration_minutes': 30,
            'calories_burned': 300,
            'distance_km': 5.0,
            'intensity': 'moderate',
            'date': timezone.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)

    def test_list_user_activities(self):
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Test Activity',
            duration_minutes=30,
            date=timezone.now()
        )
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

