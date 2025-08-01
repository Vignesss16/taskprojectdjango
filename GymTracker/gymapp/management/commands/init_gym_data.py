from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from gymapp.models import WorkoutLog, Achievement, Exercise
import random

class Command(BaseCommand):
    help = 'Initialize gym tracker with sample data and achievements'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🏋️ Initializing Gym Tracker Pro...'))
        
        # Create achievements
        self.create_achievements()
        
        # Create sample exercises
        self.create_exercises()
        
        # Create sample workout data
        self.create_sample_workouts()
        
        self.stdout.write(self.style.SUCCESS('✅ Gym Tracker Pro initialized successfully!'))

    def create_achievements(self):
        """Create default achievements"""
        achievements = [
            {
                'name': 'First Step',
                'description': 'Complete your first workout',
                'icon': '🚀',
                'requirement_type': 'total_workouts',
                'requirement_value': 1
            },
            {
                'name': 'Getting Started',
                'description': 'Complete 5 workouts',
                'icon': '💪',
                'requirement_type': 'total_workouts',
                'requirement_value': 5
            },
            {
                'name': 'Consistent',
                'description': 'Maintain a 3-day streak',
                'icon': '📅',
                'requirement_type': 'streak',
                'requirement_value': 3
            },
            {
                'name': 'Weekly Warrior',
                'description': 'Maintain a 7-day streak',
                'icon': '⚡',
                'requirement_type': 'streak',
                'requirement_value': 7
            },
            {
                'name': 'Dedication',
                'description': 'Complete 25 workouts',
                'icon': '🔥',
                'requirement_type': 'total_workouts',
                'requirement_value': 25
            },
            {
                'name': 'Century Club',
                'description': 'Complete 100 workouts',
                'icon': '💯',
                'requirement_type': 'total_workouts',
                'requirement_value': 100
            },
            {
                'name': 'Time Keeper',
                'description': 'Exercise for 60 minutes total',
                'icon': '⏰',
                'requirement_type': 'total_minutes',
                'requirement_value': 60
            },
            {
                'name': 'Hour Master',
                'description': 'Exercise for 10 hours total',
                'icon': '⏱️',
                'requirement_type': 'total_minutes',
                'requirement_value': 600
            },
            {
                'name': 'Calorie Crusher',
                'description': 'Burn 1000 calories total',
                'icon': '🔥',
                'requirement_type': 'calories_burned',
                'requirement_value': 1000
            },
            {
                'name': 'Heat Wave',
                'description': 'Burn 5000 calories total',
                'icon': '🌡️',
                'requirement_type': 'calories_burned',
                'requirement_value': 5000
            },
        ]
        
        for achievement_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            if created:
                self.stdout.write(f'Created achievement: {achievement.name}')

    def create_exercises(self):
        """Create sample exercises"""
        exercises = [
            {'name': 'Push-ups', 'category': 'Chest', 'calories_per_minute': 8.0},
            {'name': 'Squats', 'category': 'Legs', 'calories_per_minute': 6.5},
            {'name': 'Running', 'category': 'Cardio', 'calories_per_minute': 10.0},
            {'name': 'Plank', 'category': 'Core', 'calories_per_minute': 5.0},
            {'name': 'Burpees', 'category': 'Full Body', 'calories_per_minute': 12.0},
            {'name': 'Jumping Jacks', 'category': 'Cardio', 'calories_per_minute': 8.0},
            {'name': 'Pull-ups', 'category': 'Back', 'calories_per_minute': 9.0},
            {'name': 'Sit-ups', 'category': 'Core', 'calories_per_minute': 6.0},
        ]
        
        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={**exercise_data, 'description': f'{exercise_data["name"]} exercise'}
            )
            if created:
                self.stdout.write(f'Created exercise: {exercise.name}')

    def create_sample_workouts(self):
        """Create sample workout data for the last 7 days"""
        today = timezone.now().date()
        
        sample_workouts = [
            {'name': 'Morning Push Workout', 'reps': 20, 'duration': 25, 'calories': 180, 'category': 'Chest', 'intensity': 'Medium'},
            {'name': 'Core Blast', 'reps': 30, 'duration': 20, 'calories': 120, 'category': 'Core', 'intensity': 'High'},
            {'name': 'Leg Day', 'reps': 25, 'duration': 35, 'calories': 220, 'category': 'Legs', 'intensity': 'High'},
            {'name': 'Cardio Session', 'reps': 1, 'duration': 30, 'calories': 300, 'category': 'Cardio', 'intensity': 'High'},
            {'name': 'Upper Body', 'reps': 15, 'duration': 40, 'calories': 280, 'category': 'Arms', 'intensity': 'Medium'},
            {'name': 'Full Body HIIT', 'reps': 20, 'duration': 45, 'calories': 420, 'category': 'Full Body', 'intensity': 'Extreme'},
            {'name': 'Quick Stretch', 'reps': 10, 'duration': 15, 'calories': 60, 'category': 'Core', 'intensity': 'Low'},
        ]
        
        # Create workouts for the last 7 days with some variety
        for i in range(7):
            workout_date = today - timedelta(days=i)
            
            # Randomly decide if there's a workout on this day (80% chance)
            if random.random() > 0.2:
                workout = random.choice(sample_workouts)
                
                # Add some randomness to the values
                duration_variation = random.randint(-5, 10)
                calories_variation = random.randint(-20, 50)
                reps_variation = random.randint(-3, 8)
                
                WorkoutLog.objects.get_or_create(
                    workout_name=workout['name'],
                    date=workout_date,
                    defaults={
                        'reps': max(1, workout['reps'] + reps_variation),
                        'duration_minutes': max(5, workout['duration'] + duration_variation),
                        'calories_burned': max(10, workout['calories'] + calories_variation),
                        'exercise_category': workout['category'],
                        'intensity': workout['intensity'],
                        'notes': f'Sample workout for {workout_date.strftime("%B %d")}'
                    }
                )
                
                self.stdout.write(f'Created workout: {workout["name"]} for {workout_date}')
        
        # Check and award initial achievements
        self.check_initial_achievements()

    def check_initial_achievements(self):
        """Check and award achievements based on sample data"""
        from gymapp.views import check_and_update_achievements
        
        check_and_update_achievements()
        
        # Award some achievements manually for demo
        first_achievement = Achievement.objects.filter(name='First Step').first()
        if first_achievement and not first_achievement.is_earned:
            first_achievement.is_earned = True
            first_achievement.date_earned = timezone.now().date() - timedelta(days=6)
            first_achievement.save()
            self.stdout.write(f'Awarded achievement: {first_achievement.name}')
        
        getting_started = Achievement.objects.filter(name='Getting Started').first()
        if getting_started and not getting_started.is_earned:
            getting_started.is_earned = True  
            getting_started.date_earned = timezone.now().date() - timedelta(days=3)
            getting_started.save()
            self.stdout.write(f'Awarded achievement: {getting_started.name}')

# To run this command, use: python manage.py init_gym_data