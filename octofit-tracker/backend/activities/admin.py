from django.contrib import admin
from activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'activity_type', 'duration_minutes', 'date', 'intensity')
    list_filter = ('activity_type', 'intensity', 'date')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'activity_type', 'title', 'description')
        }),
        ('Metrics', {
            'fields': ('duration_minutes', 'calories_burned', 'distance_km', 'intensity')
        }),
        ('Timestamps', {
            'fields': ('date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
