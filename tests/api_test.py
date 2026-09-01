import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos/1")

data = response.json()
print(data)
print(data["title"])