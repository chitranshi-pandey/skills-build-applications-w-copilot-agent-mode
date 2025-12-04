from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from teams.models import Team, TeamMember
from teams.serializers import TeamSerializer, TeamMemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team model
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['is_public']

    def perform_create(self, serializer):
        """Set the creator to the current user when creating a team"""
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            team_member, created = TeamMember.objects.get_or_create(
                team=team,
                user=user,
                defaults={'role': role}
            )
            serializer = TeamMemberSerializer(team_member)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team_member = TeamMember.objects.get(team=team, user_id=user_id)
            team_member.delete()
            return Response({'status': 'member removed'}, status=status.HTTP_204_NO_CONTENT)
        except TeamMember.DoesNotExist:
            return Response({'error': 'member not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        """Get teams for the current user"""
        teams = Team.objects.filter(members=request.user)
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TeamMember model
    """
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

