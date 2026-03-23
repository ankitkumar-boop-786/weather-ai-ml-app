import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# Load dataset
data = pd.read_csv('../data/weather.csv')

# Features
X = data[['humidity', 'pressure', 'wind_speed', 'clouds']]

# Target
y = data['temperature']

# Model
model = RandomForestRegressor(n_estimators=100)

# Train
model.fit(X, y)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))

print("✅ Random Forest Model trained and saved successfully!")