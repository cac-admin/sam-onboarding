from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .util import store_tasks, find_schedule, validate_time
import datetime
from base.models import UserProfile, Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from myproject.settings import service
from rest_framework.authtoken.models import Token


# Create new User and UserProfile
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Request format:
    username, password, preferred_start, preferred_end
    """
    data = request.data
    username, password = data["username"], data["password"]
    preferred_start, preferred_end = data["preferred_start"], data["preferred_end"]

    # all validation: if no user exists, valid pw and username, and logical start and end preferences: register user
    try:
        User.objects.get(username=username)
        return Response("Failed: Username already exists", 400)
    except:
        if (
            username is None
            or password is None
            or len(username) < 3
            or len(password) < 5
        ):
            return Response("Invalid Username or Password", 400)

        validate_time(int(preferred_start), int(preferred_end))

        # create user, profile, and token
        
        user = User.objects.create_user(username=username, password=password)
        Token.objects.create(user=user)
        UserProfile.objects.create(
            user=user, preferred_start=preferred_start, preferred_end=preferred_end
        )
        return Response("Registration Successful", 200)


# check with User table to see if user can be authenticated
@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    data = request.data
    username, password = data["username"], data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response({
            "token": Token.objects.get(user=user).key
        }, 200)
    else:
        return Response("Authentication failed: wrong username or password", 400)


# update UserProfile fields based on new data
@api_view(["PUT"])
def update_settings(request):
    data = request.data
    """
        Request format:
        {
            "preferred_start":Int,
            "preferred_end":Int
        }

    """
    try:
        user = User.objects.get(username=request.user)
    except:
        return Response("User does not exist", 400)

    profile = UserProfile.objects.get(user=user)

    if validate_time(int(data["preferred_start"]), int(data["preferred_end"])):
        profile.preferred_start = data["preferred_start"]
        profile.preferred_end = data["preferred_end"]
        profile.save()
        return Response("Update Successful", 200)
    else:
        return Response("Invalid start/end times", 400)

"""
        - First get the events from the user, store em in Task table
        - Then run the google script to authenticate user for API
        - Then retrieve all their events in their calendar for the next week
        - Then run algorithm (new tasks are in Task table, existing events are fetched from API^)
        - The algorithm should then populate the start and end fields for each task in db
        - Then, return Schedule, which is an object containing all the tasks and their fields
"""


@api_view(["POST"])
def schedule(request):
    """
    Format of request body:
    {
        "tasks": [
            {
                "name":
                "length":
            },
            {...},
            {...}
        ]
    }
    """
    # Store user tasks in task table
    if not store_tasks(request):
        return Response(
            "Failed: Ensure that each task length is valid (under 24 hours long)", 400
        )

    # get event data for the next week
    print("Getting the upcoming 25 events")
    now = datetime.datetime.utcnow().isoformat() + "Z"
    now_dt = datetime.datetime.utcnow()
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=25,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    # Prints the start and name of next week's events
    valid_events = []
    if not events:
        print("No upcoming events found.")
    else:
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))

            # Format or start: 2023-05-05T08:00:00-04:00
            # Convert to datetime for comparison
            start_dt = datetime.datetime.strptime(start.split("T")[0], "%Y-%m-%d")

            # If it's in the next 7 days, save it
            if start_dt < now_dt.replace(day=now_dt.day + 7):
                valid_events.append(event)

    schedule = find_schedule(request.user, valid_events)
    return Response(schedule, 200)


# This route gets the confirmed Schedule object back, and calls the API to POST the final events
# The request format is the same as the returned schedule +  *** the username ***
@api_view(["POST"])
def post_tasks(request):
    tasks = request.data["tasks"]
    user = User.objects.get(username=request.user)

    for task in tasks:
        if task["start"] is not None and task["end"] is not None:
            # Format: 2023-05-09T07:00:00Z
            start_dt = datetime.datetime.strptime(task["start"], "%Y-%m-%dT%H:%M:%SZ")
            end_dt = datetime.datetime.strptime(task["end"], "%Y-%m-%dT%H:%M:%SZ")
            start = start_dt.replace(hour=start_dt.hour + 4)
            end = end_dt.replace(hour=end_dt.hour + 4)

            event = {
                "summary": task["name"],
                "start": {
                    "dateTime": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "timeZone": "America/Toronto",
                },
                "end": {
                    "dateTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "timeZone": "America/Toronto",
                },
            }
            service.events().insert(calendarId="primary", body=event).execute()

    # Now that we added the tasks to the calendar, we can rm from db
    Task.objects.filter(user=user).delete()

    return Response("Successfully added tasks to calendar!", 200)