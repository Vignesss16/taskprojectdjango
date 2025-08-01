from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Exercise(models.Model):
    """Pre-defined exercise library"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Shoulders', 'Shoulders'),
        ('Core', 'Core'),
        ('Cardio', 'Cardio'),
        ('Full Body', 'Full Body'),
    ])
    description = models.TextField()
    calories_per_minute = models.DecimalField(max_digits=4, decimal_places=1, default=5.0)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class WorkoutLog(models.Model):
    CATEGORY_CHOICES = [
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Shoulders', 'Shoulders'),
        ('Core', 'Core'),
        ('Cardio', 'Cardio'),
        ('Full Body', 'Full Body'),
    ]
    
    INTENSITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Extreme', 'Extreme'),
    ]
    
    date = models.DateField(default=timezone.now)
    workout_name = models.CharField(max_length=100)
    reps = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    exercise_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    intensity = models.CharField(max_length=20, choices=INTENSITY_CHOICES, default='Medium')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.workout_name} on {self.date}"

    class Meta:
        ordering = ['-date', '-id']


class WorkoutSchedule(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    workout_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.day}: {self.workout_name}"

class Goal(models.Model):
    goal_text = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    target_weight_loss = models.DecimalField(max_digits=5, decimal_places=2, help_text="In kilograms")
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return self.goal_text

class BodyMetrics(models.Model):
    """Track body measurements and weight"""
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="In kg")
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="In kg")
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Metrics on {self.date} - {self.weight}kg"
    
    class Meta:
        ordering = ['-date']

class Achievement(models.Model):
    """Achievement/Badge system"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')
    requirement_type = models.CharField(max_length=50, choices=[
        ('streak', 'Workout Streak'),
        ('total_workouts', 'Total Workouts'),
        ('total_minutes', 'Total Minutes'),
        ('calories_burned', 'Calories Burned'),
    ])
    requirement_value = models.IntegerField()
    date_earned = models.DateField(null=True, blank=True)
    is_earned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.icon} {self.name}"

class WorkoutSession(models.Model):
    """Track complete workout sessions"""
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=100, default="Workout Session")
    total_duration = models.PositiveIntegerField(default=0)  # in minutes
    total_calories = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} on {self.date}"