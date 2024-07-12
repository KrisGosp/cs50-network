from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.TextField(max_length=128)
    body = models.TextField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)