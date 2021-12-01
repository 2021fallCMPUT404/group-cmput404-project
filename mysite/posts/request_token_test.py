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

r = requests.post('http://127.0.0.1:8000/authors/7/posts/54/comments', auth=('admin','admin'), headers={'Referer': "http://127.0.0.1:8000/"}, data = {"type":"comment","post":54,"comment_body":"Bonk","comment_created":"2021-11-30T15:59:28.504918-07:00","id":"4a524087-f1fe-4fa0-83ee-34c01368f822"})
print(r.text)
