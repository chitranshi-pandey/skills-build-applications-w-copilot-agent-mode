from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from activities.models import Activity
from users.models import User

class LeaderboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example: Top 10 users by total activity duration
        leaderboard = (
            Activity.objects.values('user__username')
            .annotate(total_minutes=models.Sum('duration_minutes'))
            .order_by('-total_minutes')[:10]
        )
        return Response({'leaderboard': leaderboard})
