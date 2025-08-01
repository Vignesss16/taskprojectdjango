from django import forms
from .models import WorkoutLog, BodyMetrics, Goal

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout_name', 'reps', 'duration_minutes', 'calories_burned', 
                 'exercise_category', 'intensity', 'notes']
        
        widgets = {
            'workout_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Push-ups, Running, Squats',
                'id': 'id_workout_name'
            }),
            'reps': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of repetitions',
                'min': '0',
                'id': 'id_reps'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes',
                'min': '1',
                'id': 'id_duration_minutes'
            }),
            'calories_burned': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimated calories burned',
                'min': '1',
                'id': 'id_calories_burned'
            }),
            'exercise_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_exercise_category'
            }),
            'intensity': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_intensity'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes about your workout...',
                'rows': 3,
                'id': 'id_notes'
            }),
        }
        
        labels = {
            'workout_name': '💪 Workout Name',
            'reps': '🔄 Repetitions',
            'duration_minutes': '⏱️ Duration (minutes)',
            'calories_burned': '🔥 Calories Burned',
            'exercise_category': '📂 Category',
            'intensity': '⚡ Intensity',
            'notes': '📝 Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make notes field optional
        self.fields['notes'].required = False
        # Ensure category is required
        self.fields['exercise_category'].required = True

class BodyMetricsForm(forms.ModelForm):
    class Meta:
        model = BodyMetrics
        fields = ['weight', 'body_fat_percentage', 'muscle_mass', 'notes']
        
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg',
                'step': '0.1',
                'min': '30',
                'max': '300'
            }),
            'body_fat_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Body fat %',
                'step': '0.1',
                'min': '5',
                'max': '50'
            }),
            'muscle_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Muscle mass in kg',
                'step': '0.1',
                'min': '10',
                'max': '100'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes...',
                'rows': 3
            }),
        }
        
        labels = {
            'weight': '⚖️ Weight (kg)',
            'body_fat_percentage': '📊 Body Fat %',
            'muscle_mass': '💪 Muscle Mass (kg)',
            'notes': '📝 Notes',
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal_text', 'end_date', 'target_weight_loss']
        
        widgets = {
            'goal_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Lose 10kg in 3 months'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'target_weight_loss': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Target weight loss in kg',
                'step': '0.1',
                'min': '0.1'
            }),
        }
        
        labels = {
            'goal_text': '🎯 Goal Description',
            'end_date': '📅 Target Date',
            'target_weight_loss': '⚖️ Weight Loss Target (kg)',
        }


QUICK_WORKOUT_PRESETS = {
    'pushups': {
        'workout_name': 'Push-ups',
        'reps': 20,
        'duration_minutes': 10,
        'calories_burned': 50,
        'exercise_category': 'Chest',
        'intensity': 'Medium'
    },
    'squats': {
        'workout_name': 'Squats',
        'reps': 25,
        'duration_minutes': 15,
        'calories_burned': 75,
        'exercise_category': 'Legs',
        'intensity': 'Medium'
    },
    'running': {
        'workout_name': 'Running',
        'reps': 1,
        'duration_minutes': 30,
        'calories_burned': 300,
        'exercise_category': 'Cardio',
        'intensity': 'High'
    },
    'plank': {
        'workout_name': 'Plank',
        'reps': 3,
        'duration_minutes': 5,
        'calories_burned': 25,
        'exercise_category': 'Core',
        'intensity': 'Medium'
    },
    'jumping_jacks': {
        'workout_name': 'Jumping Jacks',
        'reps': 50,
        'duration_minutes': 10,
        'calories_burned': 80,
        'exercise_category': 'Cardio',
        'intensity': 'High'
    },
    'burpees': {
        'workout_name': 'Burpees',
        'reps': 15,
        'duration_minutes': 12,
        'calories_burned': 120,
        'exercise_category': 'Full Body',
        'intensity': 'High'
    }
}