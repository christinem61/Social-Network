from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name="liked_user")

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, related_name="follower_user")
    following = models.ManyToManyField(User, related_name="following_user")
