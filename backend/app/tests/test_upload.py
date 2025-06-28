import requests

url = "http://127.0.0.1:8000/upload"
file_path = "./app/tests/test_file.txt"


with open(file_path, "rb") as file:
    response = requests.post(url, data=file)

print(response.json())