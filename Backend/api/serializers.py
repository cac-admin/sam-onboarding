# We need to serialize data since the Response object cannot handle complex data types like Django models
# So we need to serialize the model outputs to JSON before sending it out

from rest_framework import serializers
# from base.models import Item

# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = '__all__'