from random import choices
from tkinter import Widget
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


CATEGORIES = (
  ('P', 'Physical'),
  ('F', 'Financial'),
  ('E', 'Education'),
  ('M', 'Mental'),
  ('O', 'Other'),
)

# Create your models here.
class Reward(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('rewards_detail', kwargs={'pk': self.id})

class Goal(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=1,
        choices=CATEGORIES,
        default=CATEGORIES[4][0]
    )
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rewards = models.ManyToManyField(Reward)
    
    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'goal_id': self.id})
    
class Update(models.Model):
    date = models.DateField()
    progress_comment = models.TextField(max_length=250)
    complete_status = models.BooleanField(
        verbose_name=("Goal Complete?"), 
        default=False,
        blank= True,
        )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE
    )  
    
    # def __str__(self):
    #     return f"{self.get_update_display()} on {self.date}"

    class Meta:
        ordering = ['-date']