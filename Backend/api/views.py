from rest_framework.response import Response
from rest_framework.decorators import api_view
# from base.models import Item
# from .serializers import ItemSerializer
from .google import Create_Service

import os


# @api_view(["GET"])
# def getData(request):
#     items = Item.objects.all()
#     serializer = ItemSerializer(items, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# def addItem(request):
#     # send data from request to the ItemSerializer class
#     serializer = ItemSerializer(data=request.data)

#     # validation
#     if serializer.is_valid():
#         serializer.save()

#     # return the data that was posted to the db
#     return Response(serializer.data)

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
        'summary': event['name'],
        'start': {
            'dateTime': event['startDateTime'],
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': event['endDateTime'],
            'timeZone': 'America/New_York',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

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
    pass



#This route gets the confirmed Schedule object back, and calls the API to POST the final events
@api_view(["POST"])
def post_tasks(request):
    pass