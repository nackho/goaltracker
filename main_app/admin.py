from django.contrib import admin
from .models import Goal, Update, Reward

# Register your models here.
admin.site.register(Goal)
admin.site.register(Update)
admin.site.register(Reward)