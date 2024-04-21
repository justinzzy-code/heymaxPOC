from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE,)
    book_id = models.PositiveIntegerField(default = 0, null=False, blank=False)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


    
    
