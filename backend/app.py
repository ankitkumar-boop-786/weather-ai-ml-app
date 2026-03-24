from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()

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
     
     input_data = pd.DataFrame([{
       "humidity": humidity,
       "pressure": pressure,
       "wind_speed": wind_speed,
       "clouds": clouds
      }])

     prediction = model.predict(input_data)
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

    data = response.json()

    if str(data.get("cod")) != "200":
      return jsonify({
        "error": data.get("message", "Weather API failed")
    })

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

    data = response.json()

    if str(data.get("cod")) != "200":
      return jsonify({
        "error": data.get("message", "Weather API failed")
    })

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    clouds = data["clouds"]["all"]

    input_data = pd.DataFrame([{
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "clouds": clouds
     }])

    prediction = model.predict(input_data)
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


port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
  