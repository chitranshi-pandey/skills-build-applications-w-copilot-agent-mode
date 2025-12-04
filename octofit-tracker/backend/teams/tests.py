from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from teams.models import Team, TeamMember

User = get_user_model()


class TeamModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            creator=self.user,
            is_public=True
        )

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.creator, self.user)
        self.assertTrue(self.team.is_public)

    def test_team_string_representation(self):
        self.assertEqual(str(self.team), 'Test Team')


class TeamViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_team(self):
        data = {
            'name': 'New Team',
            'description': 'A new team',
            'is_public': True
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_add_team_member(self):
        team = Team.objects.create(
            name='Test Team',
            creator=self.user,
            is_public=True
        )
        data = {'user_id': self.other_user.id, 'role': 'member'}
        response = self.client.post(f'/api/teams/{team.id}/add_member/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamMember.objects.count(), 1)

