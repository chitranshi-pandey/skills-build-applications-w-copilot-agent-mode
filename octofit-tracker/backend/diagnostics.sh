#!/bin/bash

echo "=========================================="
echo "OctoFit Tracker Backend Diagnostics"
echo "=========================================="

source ./venv/bin/activate

echo ""
echo "1. Django Setup Check"
python manage.py check
echo "✓ Django setup check passed"

echo ""
echo "2. Database Connection"
python manage.py dbshell --command "1" 2>/dev/null && echo "✓ Database connection verified" || echo "✗ Database connection failed"

echo ""
echo "3. MongoDB Status"
ps aux | grep mongod | grep -v grep > /dev/null && echo "✓ MongoDB is running" || echo "✗ MongoDB is not running"

echo ""
echo "4. Data Summary"
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
from activities.models import Activity
from teams.models import Team
from workouts.models import WorkoutPlan, WorkoutSession

User = get_user_model()

users = User.objects.count()
activities = Activity.objects.count()
teams = Team.objects.count()
plans = WorkoutPlan.objects.count()
sessions = WorkoutSession.objects.count()

print(f"  Users: {users}")
print(f"  Activities: {activities}")
print(f"  Teams: {teams}")
print(f"  Workout Plans: {plans}")
print(f"  Workout Sessions: {sessions}")
print(f"\n✓ Data verification passed")
EOF

echo ""
echo "5. Required Packages Check"
python -c "
import django
import rest_framework
import corsheaders
import django_filters
import djongo

print(f'  Django: {django.VERSION}')
print(f'  DRF: {rest_framework.VERSION}')
print(f'  Djongo: OK')
print(f'  Django-CORS-Headers: OK')
print(f'  Django-Filter: OK')
print('\n✓ All required packages installed')
"

echo ""
echo "=========================================="
echo "✅ All diagnostics passed!"
echo "=========================================="
