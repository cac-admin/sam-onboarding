from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer
from .Google import Create_Service


@api_view(["GET"])
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addItem(request):
    # send data from request to the ItemSerializer class
    serializer = ItemSerializer(data=request.data)

    # validation
    if serializer.is_valid():
        serializer.save()

    # return the data that was posted to the db
    return Response(serializer.data)

@api_view(["POST"])
def calendar_test(request):
    event = request.data
    
    CLIENT_SECRET_FILE = "../static/credentials.json"
    API_NAME = "calendar"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    event = {
        'summary': event.name,
        'start': {
            'dateTime': event.startDateTime,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': event.endDateTime,
            'timeZone': 'America/New_York',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    return Response("Success")