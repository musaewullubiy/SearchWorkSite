from requests import put


print(put('http://localhost:5000/api/users/1', json={
    'name': 'A',
    'surname': 'A',
    'about': 'я лох\n',
    'age': 16,
    'email': 'a@a.a',
    'hashed_password': 'pbkdf2:sha256:260000$nDPlCi9VWWCrtZZe$29db34c6ee4e6c5244bf8ff1fdac887e25a571035b03ba8fce4eb8c8d8b91fdf',
    'user_type': 'Соискатель'
}).json())