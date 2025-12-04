from django.contrib import admin
from users.models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fitness_level', 'location', 'date_joined')
    list_filter = ('fitness_level', 'date_joined')
    search_fields = ('username', 'email', 'bio')
    readonly_fields = ('date_joined', 'updated_at')
    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Profile', {
            'fields': ('bio', 'profile_image', 'fitness_level', 'location')
        }),
        ('Timestamps', {
            'fields': ('date_joined', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_steps_per_day', 'target_calories_per_day', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'goals')
    readonly_fields = ('created_at', 'updated_at')

