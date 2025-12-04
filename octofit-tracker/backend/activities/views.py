from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from activities.models import Activity
from activities.serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity model
    """
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'intensity', 'date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'duration_minutes', 'calories_burned']
    ordering = ['-date']

    def get_queryset(self):
        """Users can only view their own activities"""
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating an activity"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's activities"""
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        activities = Activity.objects.filter(
            user=request.user,
            date__date=today
        )
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def weekly_stats(self, request):
        """Get weekly statistics"""
        from django.utils import timezone
        from datetime import timedelta
        import statistics
        
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        activities = Activity.objects.filter(
            user=request.user,
            date__date__gte=week_start
        )

        total_duration = sum([a.duration_minutes for a in activities])
        total_calories = sum([a.calories_burned for a in activities if a.calories_burned])
        total_distance = sum([a.distance_km for a in activities if a.distance_km])

        return Response({
            'total_duration_minutes': total_duration,
            'total_calories': total_calories,
            'total_distance_km': total_distance,
            'activity_count': activities.count(),
        })

