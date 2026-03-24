# 🌦️ Weather AI ML App

An AI-powered weather prediction web application that combines real-time weather data with machine learning to predict temperature and analyze accuracy.

---

## 🚀 Features

* 🌍 Get real-time weather data using city name
* 🤖 Predict temperature using Machine Learning model
* 📊 Compare real vs predicted temperature
* 📈 Confidence score and prediction error
* 📉 Live prediction visualization (chart)
* 🌐 Fully deployed (Frontend + Backend)

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Backend

* Python
* Flask
* Flask-CORS

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Deployment

* Frontend: Netlify
* Backend: Render

---

## 📂 Project Structure

```
Weather_AI/
│
├── backend/
│   ├── app.py
│   ├── model/
│   ├── test.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation (Local Setup)

```bash
git clone <your-repo-url>
cd Weather_AI

# create virtual env
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run backend
cd backend
python app.py
```

---

## 🌐 API Endpoints

| Endpoint        | Method | Description                         |
| --------------- | ------ | ----------------------------------- |
| `/predict`      | POST   | Predict temperature using ML        |
| `/weather`      | GET    | Get real weather data               |
| `/predict-live` | GET    | Live prediction with real-time data |

---

## 🔐 Environment Variables

```
API_KEY=your_weather_api_key
```

---

## 📊 Example Output

```json
{
  "city": "Mumbai",
  "predicted_temp": 31.17,
  "real_temp": 30.23,
  "confidence": "95.30%",
  "prediction_error": 0.94
}
```

---

## 🚀 Live Demo

* Frontend: ["https://weather-ai-mi-app.netlify.app/"]
* Backend API: ["https://weather-ai-ml-app-9.onrender.com"]

---

## 📌 Future Improvements

* User authentication (SaaS model)
* Payment integration
* Dashboard analytics
* Mobile responsiveness improvement

---

## 👨‍💻 Author

* Ankit Kumar Yadav

---

## ⭐ If you like this project, give it a star!
