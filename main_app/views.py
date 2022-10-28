from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Goal

# Create your views here.
def home(request):
    return render(request, 'home.html')

def goals_index(request):
    goals = Goal.objects.all()
    return render(request, 'goals/index.html', { 'goals': goals })

def goals_detail(request, goal_id):
  goal = Goal.objects.get(id=goal_id)
  return render(request, 'goals/detail.html', { 'goal': goal })

class GoalCreate(CreateView):
  model = Goal
  fields = ['name', 'category', 'description', 'start_date', 'end_date']
  success_url = '/goals/'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GoalUpdate(UpdateView):
    model = Goal
    fields = ['category', 'description', 'start_date', 'end_date']

class GoalDelete(DeleteView):
    model = Goal
    success_url = '/goals/'