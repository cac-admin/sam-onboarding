from django.contrib.auth.models import User
from base.models import Task, UserProfile

# store a task in the db + validate
def store_tasks(data):
    tasks = data["tasks"]
    user = None
    # User validation check / length validation
    try:
        user = User.objects.get(username=data["user"])
        for task in tasks:
            if task["length"] > 24:
                return False
            
            Task.objects.create(user=user, name=task["name"], length=task["length"],
                    start=None, end=None)
    except:
        return False # user does not exist for one or more tasks or a task is too long
    return True


"""
    algorithm to find optimal task schedule
    parameters:
        - username: str, name of the user so we can query db for the tasks they want to do
        - events: list[] of events that the user already has in their calendar for the next week
    It populates the start and end fields for each of the user's tasks, then bundles 
    em into a schedule obj to return to the client
"""
def find_schedule(username, events):
    # start by getting the tasks from the db
    user = User.objects.get(username=username)
    tasks = Task.objects.filter(user=user)
    profile = UserProfile.objects.get(user=user)
    preferred_start = profile.preferred_start
    preferred_end = profile.preferred_end
    
    
