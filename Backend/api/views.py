from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer


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
