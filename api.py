from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load data
nhanes_file = "nhanes_data.csv"
genetic_file = "genetic_data.csv"
nhanes_data = pd.read_csv(nhanes_file)
genetic_data = pd.read_csv(genetic_file)

# Home route
@app.route('/')
def home():
    return "Welcome to the Nutritional Impact Predictor API!"

# Endpoint: Get all participants
@app.route('/participants', methods=['GET'])
def get_participants():
    participants = nhanes_data['ParticipantID'].tolist()
    return jsonify({"participants": participants})

# Endpoint: Get participant details
@app.route('/participant/<participant_id>', methods=['GET'])
def get_participant_details(participant_id):
    nhanes_info = nhanes_data[nhanes_data['ParticipantID'] == participant_id].to_dict(orient='records')
    genetic_info = genetic_data[genetic_data['ParticipantID'] == participant_id].to_dict(orient='records')

    if not nhanes_info:
        return jsonify({"error": "Participant not found in NHANES data"}), 404

    return jsonify({
        "nhanes_data": nhanes_info,
        "genetic_data": genetic_info
    })

# Endpoint: Predict long-term health impact
@app.route('/predict', methods=['POST'])
def predict_health_impact():
    data = request.get_json()
    participant_id = data.get("ParticipantID")

    nhanes_info = nhanes_data[nhanes_data['ParticipantID'] == participant_id]
    genetic_info = genetic_data[genetic_data['ParticipantID'] == participant_id]

    if nhanes_info.empty or genetic_info.empty:
        return jsonify({"error": "Participant data is incomplete or missing"}), 404

    # Dummy prediction logic (to be replaced with model integration)
    prediction = {
        "BMI": nhanes_info.iloc[0]['BMI'] + 0.5,
        "BloodPressure": nhanes_info.iloc[0]['BloodPressure'] - 1.0,
        "Impact": "Positive" if genetic_info.iloc[0]['Effect'] == "Neutral" else "Negative"
    }

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
