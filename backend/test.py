import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "humidity": 70,
    "pressure": 1012,
    "wind_speed": 3.5,
    "clouds": 40
}

response = requests.post(url, json=data)

print(response.json())