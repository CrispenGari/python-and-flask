from requests import post, get
res = post('http://localhost:5000/user/2', {"username": "username",
 "likes": 10, "comments": 15})
print(res.json())