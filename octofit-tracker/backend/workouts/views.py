from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from workouts.models import WorkoutPlan, WorkoutSession
from workouts.serializers import WorkoutPlanSerializer, WorkoutSessionSerializer


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for WorkoutPlan model
    """
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['goal', 'difficulty_level', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'duration_weeks']
    ordering = ['-created_at']

    def get_queryset(self):
        """Users can only view their own workout plans"""
        return WorkoutPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating a workout plan"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a workout plan"""
        plan = self.get_object()
        plan.is_active = True
        plan.save()
        serializer = self.get_serializer(plan)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Stop a workout plan"""
        plan = self.get_object()
        plan.is_active = False
        plan.save()
        serializer = self.get_serializer(plan)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def completion_stats(self, request, pk=None):
        """Get completion statistics for a workout plan"""
        plan = self.get_object()
        sessions = plan.sessions.all()
        completed = sessions.filter(is_completed=True).count()
        total = sessions.count()
        
        return Response({
            'total_sessions': total,
            'completed_sessions': completed,
            'completion_percentage': (completed / total * 100) if total > 0 else 0,
        })


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for WorkoutSession model
    """
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_completed']
    ordering_fields = ['day_number', 'created_at']
    ordering = ['day_number']

    def get_queryset(self):
        """Users can only view sessions from their own plans"""
        return WorkoutSession.objects.filter(workout_plan__user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a workout session as completed"""
        from django.utils import timezone
        
        session = self.get_object()
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        """Mark a workout session as incomplete"""
        session = self.get_object()
        session.is_completed = False
        session.completed_at = None
        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data)

