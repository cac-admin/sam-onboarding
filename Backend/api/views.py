from rest_framework.response import Response
from rest_framework.decorators import api_view
from .google import Create_Service
from .util import store_tasks, find_schedule
import os, datetime


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
def signup(request):
    pass


# check with User table to see if user can be authenticated
@api_view(["POST"])
def signin(request):
    pass


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
        "tasks": [
            {
                "user":
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

    tasks = request.data["tasks"]
    
    # UNCOMMENT THIS AFTER TESTING
    # Store user tasks in task table
    # if not store_tasks(tasks):
    #     return Response("Failed")
    
    # get event data for the next week
    CLIENT_SECRET_FILE = "api/credentials.json"
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    print('Getting the upcoming 25 events')
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    now_dt = datetime.datetime.utcnow()
    print(now_dt)
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=25, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Prints the start and name of next week's events
    valid_events = []
    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            # Format or start: 2023-05-05T08:00:00-04:00
            # Convert to datetime for comparison
            start_dt = datetime.datetime.strptime(start.split("T")[0], "%Y-%m-%d")

            # If it's in the next 7 days, save it
            if start_dt < now_dt.replace(day=now_dt.day+7):
                print(start, event['summary'])
                valid_events.append(event)
  
    find_schedule(tasks[0]["user"], valid_events)

    return Response("Success")


# This route gets the confirmed Schedule object back, and calls the API to POST the final events
@api_view(["POST"])
def post_tasks(request):
    pass
