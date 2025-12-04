from rest_framework import serializers
from teams.models import Team, TeamMember
from users.serializers import UserSerializer


class TeamMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for TeamMember model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'team',
            'user',
            'user_id',
            'role',
            'joined_at',
        ]
        read_only_fields = ['id', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """
    creator = UserSerializer(read_only=True)
    creator_id = serializers.IntegerField(write_only=True, required=False)
    memberships = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'description',
            'creator',
            'creator_id',
            'members',
            'memberships',
            'profile_image',
            'is_public',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
