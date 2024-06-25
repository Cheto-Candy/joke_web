from django.contrib.auth.models import User
from django.db import models

class Joke(models.Model):
    setup = models.TextField()
    punchline = models.TextField()
    fetched_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_joke = models.OneToOneField(Joke, on_delete=models.SET_NULL, null=True, blank=True)
