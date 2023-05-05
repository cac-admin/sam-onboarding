from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # should include username, uid, and pw
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) 
    # Might need gc_auth

    # will both be blank until user updates settings
    preferred_start = models.IntegerField(null=True)
    preferred_end = models.IntegerField(null=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # each task is related to a user
    name = models.CharField(max_length=100)
    length = models.IntegerField(max_length=24) # in hours

    # these are allowed to be blank (until algorithm runs)
    start = models.DateTimeField(null=True) 
    end = models.DateTimeField(null=True)