from django.core import serializers as cereal
from users.serializers import *
from django.forms.models import model_to_dict

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

def json_to_dict(queryset):
    dict_list = []
    for set in queryset:
        json_dict = model_to_dict(set)
        json_dict['actor'] = json.loads(json_dict['actor'])
        json_dict['object'] = json.loads(json_dict['object'])
        dict_list.append(json_dict)
        print(json_dict['actor'].get('fields'))
    print(dict_list)
    return dict_list