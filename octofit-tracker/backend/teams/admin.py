from django.contrib import admin
from teams.models import Team, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'description', 'creator__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TeamMemberInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'creator')
        }),
        ('Settings', {
            'fields': ('profile_image', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__username', 'team__name')
    readonly_fields = ('joined_at',)

