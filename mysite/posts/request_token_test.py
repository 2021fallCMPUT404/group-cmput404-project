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

r = requests.get('http://127.0.0.1:8000/post/request_post_list', auth=('socialdistribution_t05','c404t05'), headers={'Referer': "http://127.0.0.1:8000/"})
print(r.text)
