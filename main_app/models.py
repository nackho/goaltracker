from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Goal(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    