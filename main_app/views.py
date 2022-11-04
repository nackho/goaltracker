from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Goal, Reward
from django.contrib.auth import login
from .forms import UserForm, UpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def goals_index(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals/index.html', { 'goals': goals })

@login_required
def goals_detail(request, goal_id):
  goal = Goal.objects.get(id=goal_id)
  id_list = goal.rewards.all().values_list('id')
  rewards_goal_doesnt_have = Reward.objects.exclude(id__in=id_list)
  update_form = UpdateForm()
  return render(
    request, 
    'goals/detail.html', 
    { 'goal': goal, 
      'update_form': update_form, 
      'rewards': rewards_goal_doesnt_have
      }
    )

@login_required
def add_update(request, goal_id):
  form = UpdateForm(request.POST)
  if form.is_valid():
    new_update = form.save(commit=False)
    new_update.goal_id = goal_id
    new_update.save()
  return redirect('detail', goal_id=goal_id)

class GoalCreate(LoginRequiredMixin, CreateView):
  model = Goal
  fields = ['name', 'category', 'description', 'start_date', 'end_date']
  success_url = '/goals/'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GoalUpdate(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['category', 'description', 'start_date', 'end_date']

class GoalDelete(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = '/goals/'
    
@login_required
def assoc_reward(request, goal_id, reward_id):
  Goal.objects.get(id=goal_id).rewards.add(reward_id)
  return redirect('detail', goal_id=goal_id)

class RewardList(LoginRequiredMixin, ListView):
  model = Reward

class RewardDetail(LoginRequiredMixin, DetailView):
  model = Reward

class RewardCreate(LoginRequiredMixin, CreateView):
  model = Reward
  fields = '__all__'

class RewardUpdate(LoginRequiredMixin, UpdateView):
  model = Reward
  fields = ['name', 'description']

class RewardDelete(LoginRequiredMixin, DeleteView):
  model = Reward
  success_url = '/rewards/'
    
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def goal_progress(request, goal_id):
  template_name = "main_app/progress.html"
  current_goal = get_object_or_404(Goal, pk=goal_id)
  goal = Goal.objects.get(id=goal_id)
  available_weeks = Goal.objects.values("goal_week").filter(name=current_goal).order_by("goal_week").distinct() 
  context = { "goal" : goal, "available_weeks" : available_weeks}

  return render (request, template_name, context)

def weekly_progress(request, goal_id):
  template_name = "main_app/weekly_progress.html"
  current_goal = get_object_or_404(Goal, pk=goal_id)
  goal_week_input = request.POST.get("goal_week_input", False)
  available_weeks = Goal.objects.values("goal_week").filter(name=current_goal).order_by("goal_week").distinct() 

  goals = Goal.objects.filter(name=current_goal, goal_week=goal_week_input)

  context = {'current_goal': current_goal, 'goals': goals, 'goal_week_input': goal_week_input, 'available_weeks': available_weeks}

  return render (request, template_name, context)

def range_progress(request, goal_id):
  current_goal = get_object_or_404(Goal, pk=goal_id)
  available_weeks = Goal.objects.values("goal_week").filter(name=current_goal).order_by("goal_week").distinct() 

  start_week = request.POST.get("start_week", False)
  start_week = int(start_week)

  end_week = request.POST.get("end_week", False)
  end_week = int(end_week)

  week_range = list(range(start_week, end_week+1))

  weekly_goal = []

  for week in week_range:
    weekly_goal.append(Goal.objects.filter(goal_week=week, name=current_goal))

  context = {'current_goal': current_goal, 'available_weeks': available_weeks, 'week_range': week_range, 'start_week': start_week, 'end_week': end_week}

  return render(request, "main_app/range_progress.html", context)
