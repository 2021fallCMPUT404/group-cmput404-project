from django.shortcuts import get_object_or_404
from posts.models import Node
from users.models import User
import requests
from posts.serializers import NodeSerializer

#This function will check if the id is a local user
def is_local_id(user_id):
    user = User.objects.filter(pk=user_id)
    if user != None:
        return True
    else:
        return False

# This function will check if the id given is on a foreign server.
# It will return a tuple, with the first value being a bool, the 2nd a url string
# Returns true with the url if it is a valid foreign id, else, returns False with None

def make_external_request(url, auth, method='GET'):
    headers = {'Referer': "http://127.0.0.1:8000/"}
    if method == "GET":
        ext_request = requests.get(url, auth=auth, headers=headers)
    elif method == "POST":
        ext_request = requests.post(url, auth=auth, headers=headers)
    elif method == "PUT":
        ext_request = requests.put(url, auth=auth, headers=headers)
    elif method == "DELETE":
        ext_request = requests.delete(url, auth=auth, headers=headers)
    else:
        return Exception

    #ext_request = ext_request.json()
    return ext_request

def get_nodes():
    nodes = Node.objects.all()
    serializer = NodeSerializer(nodes, many=True)
    connected = []
    for node in serializer.data:
        connected.append(node)
    return connected


def is_foreign_id(user_id):
    
    nodes = get_nodes()
    print("PRINTING NODES: {}".format(nodes))
    for node in nodes:
        url = '{}author/'.format(node['url'], user_id)
        print(url)
        request = make_external_request(url, (node['username'], node['password']))
        if request.status_code != 200:
            break
        authors = request.json()['items']
        print(authors)
        try:
            # Reference: http://127.0.0.1:8000/post/test/e0f090d4-7af3-49de-8f2b-fee29a8d98e8/
            test = list(filter(lambda author: user_id in author['id'], authors))
            print("Filter object: ", test)
            if test != None:
                return (True, test[0])
        except Exception as e:
            print("Error: {}".format(e))
    return (False, None)


def get_foreign_authors_list():
    nodes = get_nodes()
    for node in nodes:
        url = '{}authors/?size=10000'.format(node['url'])
        print(url)
        request = make_external_request(url, (node['username'], node['password']))
        if request.status_code != 200:
            print("Status code: {}".format(request.status_code))
    return request.json()['items']

def make_external_friend_request(internal_id, foreign_id):
    foreign_host = is_foreign_id(foreign_id)[1]['host'] + 'service/'
    print('Printing foreign host: {}'.format(foreign_host)) 
    node = get_object_or_404(Node, url=foreign_host)
    url = '{}author/{}/followers/{}'.format(foreign_host, foreign_id, internal_id)
    print("THE URL", url)
    request = make_external_request(url, (node.username, node.password), method='PUT')
    print(request)
    return request.status_code