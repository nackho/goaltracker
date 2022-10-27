from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('goals/', views.goals_index, name='index'),
    path('goals/<int:goal_id>/', views.goals_detail, name='detail'),
]