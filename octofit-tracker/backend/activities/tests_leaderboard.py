from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from activities.models import Activity

class LeaderboardAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        Activity.objects.create(user=self.user1, activity_type='running', title='Run', duration_minutes=60, date='2025-12-01T10:00:00Z')
        Activity.objects.create(user=self.user2, activity_type='cycling', title='Cycle', duration_minutes=120, date='2025-12-01T11:00:00Z')

    def test_leaderboard(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('leaderboard', response.data)
        self.assertTrue(any(entry['user__username'] == 'user2' for entry in response.data['leaderboard']))
