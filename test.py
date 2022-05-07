from requests import post, get, delete

print(delete('http://127.0.0.1:5000/api/appointment/1').json())
