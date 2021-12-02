import requests
import ast, json
'''
url = 'https://cmput404-socialdist-project.herokuapp.com/api-token-auth/'
headers = {"username": "a", "password": "a"}
response = requests.post(url, json=headers)
print(response.text)
token = ast.literal_eval(response.text)['token']
'''

url = 'http://127.0.0.1:8000/post/request_post_list'

r = requests.put('http://127.0.0.1:8000/authors/7/posts/54',
                 data={
                     "type": "post",
                     "id": 54,
                     "title":
                     "Test if request user name malstches author name",
                     "text": "Go to horny jail",
                     "image": None,
                     "pub_date": "2021-11-30T00:32:10.930002-07:00",
                     "author": {
                         "username": "1",
                         "first_name": "1",
                         "last_name": "1",
                         "email": "1@ualberta.ca"
                     },
                     "shared_user": None,
                     "shared_on": None,
                     "privacy": 0,
                     "contentType": 0
                 })
print(r.text)
