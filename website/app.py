from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import requests

# Initialize Flask app
app = Flask(__name__)

# Load dataset and preprocess it
dataset = pd.read_csv('dataset.csv')
dataset = pd.get_dummies(dataset, columns=['State', 'Crop'], drop_first=True)
dataset = dataset.dropna()

X = dataset.drop(['Yield', 'Price'], axis=1)
y_yield = dataset['Yield']
y_price = dataset['Price']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train models
yield_model = LinearRegression()
yield_model.fit(X_scaled, y_yield)

price_model = LinearRegression()
price_model.fit(X_scaled, y_price)

# Function to predict yield and price
def predict_crop(crop_name):
    # Normalize crop name (to handle case-insensitive matching)
    crop_name = crop_name.strip().capitalize()  # Capitalize the first letter and strip any extra spaces
    crop_column = f'Crop_{crop_name.upper()}'  # Make sure to match the column name format (uppercase)

    # Print the crop column being looked for (for debugging)
    print(f"Looking for column: {crop_column}")

    # Check if the crop column exists in the dataset columns
    if crop_column not in X.columns:
        return f"Error: Crop '{crop_name}' is not available in the dataset. Available crops: {', '.join(X.columns)}"

    # Create a new data row for prediction (ensure all columns are initially set to 0)
    new_data = pd.DataFrame(columns=X.columns)
    new_data.loc[0] = 0  # Set all features to 0
    new_data[crop_column] = 1  # Set the relevant crop column to 1

    # Scale the new data using the same scaler as the training data
    new_data_scaled = scaler.transform(new_data)

    # Predict yield and price
    predicted_yield = yield_model.predict(new_data_scaled)[0]
    predicted_price = price_model.predict(new_data_scaled)[0]

    return predicted_yield, predicted_price

# Function to send SMS using Fast2SMS
def send_sms(phone_number, message):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = {
        'sender_id': 'FSTSMS',
        'message': message,
        'language': 'english',
        'route': 'p',
        'numbers': phone_number,
    }
    headers = {
        'authorization': 'KQPBiCoRyqczhdYwAklt7SJ4VDx5gLeEXTGa139ruM6IUH208WbPDdXCkZwF7EIMnGesYL6mcrRU4QxW'  # Replace with your Fast2SMS API key
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.status_code == 200

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction and SMS API
@app.route('/predict', methods=['POST'])
def predict():
    crop = request.form['crop_name'].lower()  # Take input as lowercase
    phone_number = request.form['phone_number']

    # Predict crop yield and price
    prediction = predict_crop(crop)
    
    # If the prediction returns an error message
    if isinstance(prediction, str):
        return render_template('index.html', message=prediction)

    # Get the predicted yield and price
    predicted_yield, predicted_price = prediction
    
    # Prepare the message for the user
    message = f"Dear Farmer, the predicted yield for {crop.capitalize()} is {predicted_yield:.2f} quintals/ha, and the predicted price is {predicted_price:.2f} INR."

    # Send SMS to the provided phone number
    sms_status = send_sms(phone_number, message)
    sms_message = "SMS sent successfully!" if sms_status else "Failed to send SMS."

    # Return the rendered template with the results and SMS status
    return render_template(
        'index.html',
        predicted_yield=f"{predicted_yield:.2f}",
        predicted_price=f"{predicted_price:.2f}",
        sms_message=sms_message
    )

if __name__ == '__main__':
    app.run(debug=True)
