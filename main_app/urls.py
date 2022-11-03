from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('goals/', views.goals_index, name='index'),
    path('goals/<int:goal_id>/', views.goals_detail, name='detail'),
    path('goals/create/', views.GoalCreate.as_view(), name='goals_create'),
    path('goals/<int:pk>/update/', views.GoalUpdate.as_view(), name='goals_update'),
    path('goals/<int:pk>/delete/', views.GoalDelete.as_view(), name='goals_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('goals/<int:goal_id>/add_update/', views.add_update, name='add_update'),
    path('rewards/', views.RewardList.as_view(), name='rewards_index'),
    path('rewards/<int:pk>/', views.RewardDetail.as_view(), name='rewards_detail'),
    path('rewards/create/', views.RewardCreate.as_view(), name='rewards_create'),
    path('rewards/<int:pk>/update/', views.RewardUpdate.as_view(), name='rewards_update'),
    path('rewards/<int:pk>/delete/', views.RewardDelete.as_view(), name='rewards_delete'),
    path('goals/<int:goal_id>/assoc_reward/<int:reward_id>/', views.assoc_reward, name='assoc_reward'),
    path('goals/<int:goal_id>/progress/', views.goal_progress, name='goal_progress'),
]