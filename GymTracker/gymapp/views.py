from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import WorkoutLog, Achievement, BodyMetrics, Goal
from .forms import WorkoutLogForm

def dashboard(request):
    """Dashboard view with overview stats"""
    today = timezone.now().date()
    
    # Get recent workouts
    workouts = WorkoutLog.objects.all().order_by('-date')[:5]
    total_workouts = WorkoutLog.objects.count()
    
    # Today's stats
    today_workouts = WorkoutLog.objects.filter(date=today)
    today_calories = today_workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    daily_minutes = today_workouts.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
    
    # Calculate streak
    streak = calculate_workout_streak()
    
    # Weekly chart data
    chart_labels, chart_data = get_weekly_chart_data()
    
    # Progress calculation
    daily_goal = 60
    daily_progress_percentage = min((daily_minutes / daily_goal) * 100, 100) if daily_goal > 0 else 0
    
    # Recent achievements
    recent_achievements = Achievement.objects.filter(is_earned=True).order_by('-date_earned')[:3]
    
    context = {
        'workouts': workouts,
        'today_calories': today_calories,
        'daily_minutes': daily_minutes,
        'daily_goal': daily_goal,
        'streak': streak,
        'total_workouts': total_workouts,
        'daily_progress_percentage': daily_progress_percentage,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'recent_achievements': recent_achievements,
    }
    
    return render(request, 'gymapp/dashboard.html', context)

def add_workout(request):
    """Add workout view"""
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Workout added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WorkoutLogForm()
    
    return render(request, 'gymapp/add_workout.html', {'form': form})

def analytics(request):
    """Analytics view"""
    workouts = WorkoutLog.objects.all().order_by('-date')
    
    # Total statistics
    total_stats = WorkoutLog.objects.aggregate(
        total_minutes=Sum('duration_minutes'),
        total_calories=Sum('calories_burned'),
        total_workouts=Count('id'),
        avg_minutes=Avg('duration_minutes')
    )
    
    # Monthly data for chart
    monthly_labels, monthly_data = get_monthly_chart_data()
    
    # Category breakdown
    category_data = get_category_breakdown()
    
    context = {
        'workouts': workouts,
        'total_minutes': total_stats['total_minutes'] or 0,
        'total_calories': total_stats['total_calories'] or 0,
        'total_workouts': total_stats['total_workouts'] or 0,
        'average_minutes_per_workout': round(total_stats['avg_minutes'] or 0, 1),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_data': json.dumps(monthly_data),
        'category_data': json.dumps(category_data),
    }
    
    return render(request, 'gymapp/analytics.html', context)

def achievements(request):
    """Achievements view"""
    earned_achievements = Achievement.objects.filter(is_earned=True).order_by('-date_earned')
    available_achievements = Achievement.objects.filter(is_earned=False)
    
    context = {
        'earned_achievements': earned_achievements,
        'available_achievements': available_achievements,
    }
    
    return render(request, 'gymapp/achievements.html', context)

def timer(request):
    """Timer view"""
    return render(request, 'gymapp/timer.html')

def calculate_workout_streak():
    today = timezone.now().date()
    streak = 0
    current_date = today
    
    while streak < 365:
        if WorkoutLog.objects.filter(date=current_date).exists():
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

def get_weekly_chart_data():
    today = timezone.now().date()
    week_start = today - timedelta(days=6)
    
    labels = []
    data = []
    
    for i in range(7):
        date = week_start + timedelta(days=i)
        labels.append(date.strftime('%a'))
        
        daily_minutes = WorkoutLog.objects.filter(date=date).aggregate(
            Sum('duration_minutes')
        )['duration_minutes__sum'] or 0
        
        data.append(daily_minutes)
    
    return labels, data

def get_monthly_chart_data():
    today = timezone.now().date()
    months = []
    data = []
    
    for i in range(6):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        months.append(month_date.strftime('%b'))
        
        monthly_minutes = WorkoutLog.objects.filter(
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        
        data.append(monthly_minutes)
    
    return list(reversed(months)), list(reversed(data))

def get_category_breakdown():
    categories = WorkoutLog.objects.values('exercise_category').annotate(
        total_minutes=Sum('duration_minutes')
    ).order_by('-total_minutes')
    
    return {cat['exercise_category']: cat['total_minutes'] for cat in categories}