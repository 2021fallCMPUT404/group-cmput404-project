import requests
import json




def get_authors(url):

    ext_request = requests.get(url, auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:8000/"})

    ext_request = ext_request.json()
    

    return ext_request


e = get_authors( "https://unhindled.herokuapp.com/service/authors")

for i in e['items']:
    print(i)