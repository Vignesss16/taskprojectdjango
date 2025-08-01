from django.contrib import admin
from .models import WorkoutLog, Exercise, WorkoutSchedule, Goal, BodyMetrics, Achievement, WorkoutSession

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ['workout_name', 'date', 'duration_minutes', 'calories_burned', 'intensity', 'exercise_category']
    list_filter = ['date', 'intensity', 'exercise_category']
    search_fields = ['workout_name', 'notes']
    ordering = ['-date', '-id']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Workout Details', {
            'fields': ('workout_name', 'exercise_category', 'intensity')
        }),
        ('Metrics', {
            'fields': ('reps', 'duration_minutes', 'calories_burned')
        }),
        ('Additional Info', {
            'fields': ('date', 'notes'),
            'classes': ('collapse',)
        })
    )

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories_per_minute']
    list_filter = ['category']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'requirement_type', 'requirement_value', 'is_earned', 'date_earned']
    list_filter = ['requirement_type', 'is_earned']
    search_fields = ['name', 'description']
    ordering = ['requirement_type', 'requirement_value']
    
    fieldsets = (
        ('Achievement Info', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Requirements', {
            'fields': ('requirement_type', 'requirement_value')
        }),
        ('Status', {
            'fields': ('is_earned', 'date_earned')
        })
    )

@admin.register(BodyMetrics)
class BodyMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'weight', 'body_fat_percentage', 'muscle_mass']
    ordering = ['-date']
    date_hierarchy = 'date'

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['goal_text', 'start_date', 'end_date', 'target_weight_loss', 'is_achieved']
    list_filter = ['is_achieved', 'start_date']
    ordering = ['-start_date']

@admin.register(WorkoutSchedule)
class WorkoutScheduleAdmin(admin.ModelAdmin):
    list_display = ['day', 'workout_name']
    ordering = ['day']

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'total_duration', 'total_calories']
    ordering = ['-date']
    date_hierarchy = 'date'