from django.core import serializers as cereal
from users.serializers import *

def serialize_object(object):
    serialized_object = cereal.serialize('json', [object]).replace("[","").replace("]","")
    return serialized_object

def queryset_to_json(queryset):
    query_list = []
    for set in queryset:
        serializer = friend_request_serializer(instance=set)
        query_list.append(serializer.data)
    return query_list

def followers_to_json(queryset):
    query_list = []
    for set in queryset:
        serializer = userFollowSerializer(instance=set)
        query_list.append(serializer.data)
    return query_list