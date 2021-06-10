import requests
url = "http://127.0.0.1:5000/"
res = requests.get(url)
print(res.json())

if __name__=="__main__":
    pass