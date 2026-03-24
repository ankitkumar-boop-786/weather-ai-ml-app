from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import requests
import re
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

CORS(app)


model = pickle.load(open('model/model.pkl', 'rb'))
@app.route('/')
def home():
    return "API is running 🚀"

@app.route('/predict', methods=['POST'])

def predict():
    try:
     data = request.json

     humidity = data.get('humidity')
     pressure = data.get('pressure')
     wind_speed = data.get('wind_speed', 0)
     clouds = data.get('clouds', 0)
     
     prediction = model.predict([[humidity, pressure, wind_speed, clouds]])
     return jsonify({'temperature': prediction[0]})
    except Exception as e:
        return jsonify({
            "error": "Invalid input data",
            "details": str(e)
        })

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
     return jsonify({"error": "Weather API failed"})
    
    data = response.json()

    if "main" not in data:
      return jsonify({"error": "Invalid city name"})

    return jsonify({

    "temperature": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "pressure": data["main"]["pressure"],
    "wind_speed": data["wind"]["speed"],
    "clouds": data["clouds"]["all"]
})

@app.route('/predict-live', methods=['GET'])
def predict_live():
    city = request.args.get('city')
    if not city or not re.match("^[a-zA-Z ]+$", city):
     return jsonify({
        "error": "Invalid city name. Only letters allowed."
    })

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
     return jsonify({"error": "Weather API failed"})
    
    data = response.json()

    if "main" not in data:
     return jsonify({"error": "Invalid city name"})

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    clouds = data["clouds"]["all"]

    prediction = model.predict([[humidity, pressure, wind_speed, clouds]])
    error = abs(data["main"]["temp"] - prediction[0])
    confidence = max(0, 100 - (error * 5))
   
    return jsonify({
    "city": city,
    "real_temp": data["main"]["temp"],
    "predicted_temp": prediction[0],
    "prediction_error": error,
    "confidence": f"{confidence:.2f}%",
    "humidity": humidity,
    "pressure": pressure,
    "wind_speed": wind_speed,
    "clouds": clouds,
    
})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  