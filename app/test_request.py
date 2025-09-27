import requests

# Send text string to localhost
response = requests.post(
    "http://127.0.0.1:8000/api/predict",
    json={"input": "молоко 2"}
)

print("Response:", response.json())

response2 = requests.post(
    "http://127.0.0.1:8000/api/predict",
    json={"input": ""}
)

print("Response 2:", response2.json())