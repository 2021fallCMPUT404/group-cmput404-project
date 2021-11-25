import requests

#url = 'http://127.0.0.1:8000/api-token-auth/'
url = 'http://127.0.0.1:8000/post/request_post_list'
data = {"username": "1"}
#r = requests.post(url, json=data)
r = requests.get(url, headers=data)
print(r.text)