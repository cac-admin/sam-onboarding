from rest_framework.response import Response
from rest_framework.decorators import api_view
from .google import Create_Service
from .util import store_tasks, find_schedule
import os, datetime
from base.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


@api_view(["POST"])
def calendar_test(request):
    """
    Example request body (JSON):
    {
        "name":"calendar Test",
        "startDateTime":"2023-05-04T09:00:00-07:00",
        "endDateTime":"2023-05-04T09:00:00-07:00"
    }
    """

    event = request.data
    print(os.getcwd())
    CLIENT_SECRET_FILE = "api/credentials.json"
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    event = {
        "summary": event["name"],
        "start": {
            "dateTime": event["startDateTime"],
            "timeZone": "America/New_York",
        },
        "end": {
            "dateTime": event["endDateTime"],
            "timeZone": "America/New_York",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()

    return Response("Success")


# Create new User and UserProfile
@api_view(["POST"])
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
        return Response("Failed: Username already exists")
    except:
        if (
            username is None
            or password is None
            or len(username) < 3
            or len(password) < 5
        ):
            return Response("Invalid Username or Password")

        if (
            preferred_start < 0
            or preferred_start > 24
            or preferred_end < 0
            or preferred_end > 24
            or preferred_end < preferred_start
        ):
            return Response("Invalid preferred start/end times")

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(
            user=user, preferred_start=preferred_start, preferred_end=preferred_end
        )
        return Response("Registration Successful")


# check with User table to see if user can be authenticated
@api_view(["POST"])
def signin(request):
    data = request.data
    username, password = data["username"], data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        return Response("Authenticated")
    else:
        return Response("Authentication failed: wrong username or password")


# update UserProfile fields based on new data
@api_view(["UPDATE"])
def update_settings(request):
    pass


"""
    This one will be a big one:
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
        "user": "username",
        "tasks": [
            {
                "name":
                "length":
                "start": NULL
                "end": NULL
            },
            {...},
            {...}
        ]
    }
    """

    data = request.data

    # UNCOMMENT THIS AFTER TESTING
    # Store user tasks in task table
    if not store_tasks(data):
        return Response("Failed")

    # get event data for the next week
    CLIENT_SECRET_FILE = "api/credentials.json"
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    print("Getting the upcoming 25 events")
    now = datetime.datetime.utcnow().isoformat() + "Z"
    now_dt = datetime.datetime.utcnow()
    # print(now_dt)
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
                # print(start, event["summary"])
                valid_events.append(event)

    # schedule = find_schedule(data["user"], valid_events)
    schedule = find_schedule(data["user"], valid_events)
    return Response(schedule)


# This route gets the confirmed Schedule object back, and calls the API to POST the final events
@api_view(["POST"])
def post_tasks(request):
    pass
