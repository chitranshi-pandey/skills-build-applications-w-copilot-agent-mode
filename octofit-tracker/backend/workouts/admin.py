from django.contrib import admin
from workouts.models import WorkoutPlan, WorkoutSession


class WorkoutSessionInline(admin.TabularInline):
    model = WorkoutSession
    extra = 1


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'goal', 'difficulty_level', 'is_active', 'created_at')
    list_filter = ('goal', 'difficulty_level', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WorkoutSessionInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Plan Details', {
            'fields': ('goal', 'difficulty_level', 'duration_weeks', 'workouts_per_week')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'workout_plan', 'day_number', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('title', 'description', 'workout_plan__title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('workout_plan', 'day_number', 'title', 'description')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'exercises')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

