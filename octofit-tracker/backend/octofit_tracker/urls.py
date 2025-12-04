"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os

# Import ViewSets
from users.views import UserViewSet, UserProfileViewSet
from activities.views import ActivityViewSet
from teams.views import TeamViewSet, TeamMemberViewSet
from workouts.views import WorkoutPlanViewSet, WorkoutSessionViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'team-members', TeamMemberViewSet, basename='team-member')
router.register(r'workout-plans', WorkoutPlanViewSet, basename='workout-plan')
router.register(r'workout-sessions', WorkoutSessionViewSet, basename='workout-session')


@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'users': f'{base_url}/api/users/',
            'activities': f'{base_url}/api/activities/',
            'teams': f'{base_url}/api/teams/',
            'workouts': f'{base_url}/api/workout-plans/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
