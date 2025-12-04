import os
import django
from django.utils import timezone
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from django.contrib.auth import get_user_model
from activities.models import Activity
from teams.models import Team, TeamMember
from workouts.models import WorkoutPlan, WorkoutSession
from users.models import UserProfile

User = get_user_model()

# Clear existing data
print("Clearing existing test data...")
User.objects.all().delete()
Activity.objects.all().delete()
Team.objects.all().delete()
WorkoutPlan.objects.all().delete()
WorkoutSession.objects.all().delete()

# Create test users
print("Creating test users...")
users = []
user_data = [
    {'username': 'alice', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Smith'},
    {'username': 'bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
    {'username': 'charlie', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
    {'username': 'diana', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Prince'},
    {'username': 'evan', 'email': 'evan@example.com', 'first_name': 'Evan', 'last_name': 'Davis'},
]

for data in user_data:
    user = User.objects.create_user(
        password='testpass123',
        fitness_level=random.choice(['beginner', 'intermediate', 'advanced']),
        location=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
        bio=f"Fitness enthusiast and athlete",
        **data
    )
    users.append(user)
    print(f"  Created user: {user.username}")

# Create user profiles
print("Creating user profiles...")
for user in users:
    UserProfile.objects.create(
        user=user,
        goals=f"Get fit and maintain a healthy lifestyle",
        target_steps_per_day=random.randint(8000, 15000),
        target_calories_per_day=random.randint(1800, 2500),
    )
    print(f"  Created profile for: {user.username}")

# Create activities
print("Creating activities...")
activity_types = ['running', 'walking', 'cycling', 'swimming', 'gym', 'yoga', 'sports']
intensities = ['low', 'moderate', 'high']

for user in users:
    for i in range(random.randint(5, 10)):
        days_ago = random.randint(0, 30)
        activity_date = timezone.now() - timedelta(days=days_ago)
        
        activity = Activity.objects.create(
            user=user,
            activity_type=random.choice(activity_types),
            title=f"Activity {i+1}",
            description=f"Great workout session",
            duration_minutes=random.randint(20, 120),
            calories_burned=random.randint(100, 500),
            distance_km=round(random.uniform(1.0, 10.0), 2),
            intensity=random.choice(intensities),
            date=activity_date,
        )
        print(f"  Created activity: {activity.title} for {user.username}")

# Create teams
print("Creating teams...")
teams = []
team_names = [
    'Morning Runners',
    'Gym Warriors',
    'Cycling Enthusiasts',
    'Yoga Masters',
    'Fitness Champions',
]

for name in team_names:
    team = Team.objects.create(
        name=name,
        description=f"A community of {name.lower()} passionate about fitness",
        creator=random.choice(users),
        is_public=True,
    )
    teams.append(team)
    print(f"  Created team: {name}")

# Add members to teams
print("Adding members to teams...")
for team in teams:
    # Add random members (excluding creator)
    members_to_add = random.sample(users, random.randint(2, 4))
    for user in members_to_add:
        if user != team.creator:
            TeamMember.objects.create(
                team=team,
                user=user,
                role=random.choice(['admin', 'coach', 'member']),
            )
            print(f"  Added {user.username} to team {team.name}")

# Create workout plans
print("Creating workout plans...")
goals = ['weight_loss', 'muscle_gain', 'endurance', 'flexibility', 'general_fitness']
difficulty_levels = ['beginner', 'intermediate', 'advanced']

for user in users:
    for i in range(random.randint(1, 3)):
        plan = WorkoutPlan.objects.create(
            user=user,
            title=f"Workout Plan {i+1}",
            description=f"A personalized fitness program for {user.username}",
            goal=random.choice(goals),
            difficulty_level=random.choice(difficulty_levels),
            duration_weeks=random.choice([4, 8, 12, 16]),
            workouts_per_week=random.randint(3, 6),
            is_active=random.choice([True, False]),
        )
        print(f"  Created workout plan: {plan.title} for {user.username}")
        
        # Create workout sessions for the plan
        for day in range(1, random.randint(3, 6)):
            session = WorkoutSession.objects.create(
                workout_plan=plan,
                day_number=day,
                title=f"Day {day} Workout",
                description=f"Workout session for day {day}",
                duration_minutes=random.randint(30, 90),
                exercises=[
                    {"name": "Warm-up", "duration": 5},
                    {"name": "Main Exercise", "duration": 40},
                    {"name": "Cool-down", "duration": 5},
                ],
                is_completed=random.choice([True, False]),
            )
            if session.is_completed:
                session.completed_at = timezone.now() - timedelta(days=random.randint(0, 7))
                session.save()
            print(f"    Created session: {session.title}")

print("\n✅ Database population complete!")
print(f"Created {User.objects.count()} users")
print(f"Created {Activity.objects.count()} activities")
print(f"Created {Team.objects.count()} teams")
print(f"Created {TeamMember.objects.count()} team memberships")
print(f"Created {WorkoutPlan.objects.count()} workout plans")
print(f"Created {WorkoutSession.objects.count()} workout sessions")
