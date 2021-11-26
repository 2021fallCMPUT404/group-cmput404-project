import requests
def get_t15_posts(url):

    ext_request = requests.get(url, auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:8000/"})

    ext_request = ext_request.json()
    return ext_request[0]

url = get_t15_posts('https://unhindled.herokuapp.com/service/allposts/')


auth = url['author']
print(auth['username'])


