from django.contrib.auth.models import User
from django.db import models
from base.models import Task

# store a task in the db + validate
def store_tasks(tasks):

    # User validation check / length validation
    try:
        for task in tasks:
            user = User.objects.get(username=task["user"])
            task["user"] = user
            if task["length"] > 24:
                return False
    except:
        return False # user does not exist for one or more tasks or a task is too long
    
    # actually store tasks if they're all valid
    for task in tasks:
        Task.objects.create(user=task["user"], name=task["name"], length=task["length"],
                            start=None, end=None)
    return True
