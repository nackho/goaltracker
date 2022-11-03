from django.shortcuts import render, redirect
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


    
