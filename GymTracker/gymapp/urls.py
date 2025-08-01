from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-workout/', views.add_workout, name='add_workout'),
    path('analytics/', views.analytics, name='analytics'),
    path('achievements/', views.achievements, name='achievements'),
    path('timer/', views.timer, name='timer'),
]