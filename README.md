🌾 Crop Yield & Price Predictor with SMS Notification
This Flask-based web application allows farmers to predict the yield and price of a selected crop using a trained machine learning model. The application also sends the prediction results to a farmer’s phone via SMS using the Fast2SMS API.

🚀 Features
Predicts crop yield (quintals/hectare) and price (INR).

Input crop name and phone number via a simple web interface.

Sends prediction results to the entered phone number via SMS.

Handles errors like unsupported crop names gracefully.

🧠 Technologies Used
Flask – Web framework

Pandas & NumPy – Data manipulation

Scikit-learn – ML modeling (Linear Regression & StandardScaler)

Fast2SMS API – SMS integration

HTML (Jinja2 templates) – Frontend

📁 File Structure
php
Copy
Edit
├── app.py                # Main Flask app
├── dataset.csv           # Dataset used for model training
├── templates/
│   └── index.html        # Frontend HTML form
├── static/               # (Optional) For CSS/JS/images
└── README.md             # This file
🛠️ How to Run Locally
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/crop-yield-price-predictor.git
cd crop-yield-price-predictor
2. Install Dependencies
Make sure Python 3.7+ is installed.

bash
Copy
Edit
pip install flask pandas numpy scikit-learn requests
3. Add Your Fast2SMS API Key
In app.py, replace the authorization field under headers with your actual Fast2SMS API key:

python
Copy
Edit
'authorization': 'YOUR_FAST2SMS_API_KEY'
4. Prepare the Dataset
Ensure that dataset.csv is in the root directory and contains at least the following columns:

Yield

Price

State (categorical)

Crop (categorical)

Any other numerical/categorical features (these will be one-hot encoded).

5. Run the Application
bash
Copy
Edit
python app.py
Visit http://127.0.0.1:5000 in your browser.

📦 Example Use Case
Open the app in your browser.

Enter a crop name (e.g., "Wheat") and your phone number.

Click Predict.

Get instant predictions on the screen and an SMS sent to your phone!

📌 Notes
Make sure the crop name exists in your dataset. The app will notify you if it doesn't.

SMS functionality requires internet access and a valid Fast2SMS API key.

This is a basic model. For production use, consider more advanced modeling techniques and security improvements.

💡 Future Improvements
Add more models (RandomForest, XGBoost) for better accuracy.

Include user login and history of predictions.

Support for regional languages in SMS.

Add crop image upload and recognition.

📬 Contact
For questions, issues, or contributions, feel free to open an issue or contact [your-email@example.com].
