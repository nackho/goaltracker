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
class Goal(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=100,
        choices=CATEGORIES,
        default=CATEGORIES[4][0]
    )
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_category_display()}"
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'goal_id': self.id})
    
class Update(models.Model):
    date = models.DateField()
    progress_comment = models.TextField(max_length=250)
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE
    )  