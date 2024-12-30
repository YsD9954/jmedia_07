# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pandas as pd

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable Cross-Origin Resource Sharing

# # Load data
# nhanes_file = "nhanes_data.csv"
# genetic_file = "genetic_data.csv"
# nhanes_data = pd.read_csv(nhanes_file)
# genetic_data = pd.read_csv(genetic_file)

# # Home route
# @app.route('/')
# def home():
#     return "Welcome to the Nutritional Impact Predictor API!"

# # Endpoint: Get all participants
# @app.route('/participants', methods=['GET'])
# def get_participants():
#     participants = nhanes_data['ParticipantID'].tolist()
#     return jsonify({"participants": participants})

# # Endpoint: Get participant details
# @app.route('/participant/<participant_id>', methods=['GET'])
# def get_participant_details(participant_id):
#     nhanes_info = nhanes_data[nhanes_data['ParticipantID'] == participant_id].to_dict(orient='records')
#     genetic_info = genetic_data[genetic_data['ParticipantID'] == participant_id].to_dict(orient='records')

#     if not nhanes_info:
#         return jsonify({"error": "Participant not found in NHANES data"}), 404

#     return jsonify({
#         "nhanes_data": nhanes_info,
#         "genetic_data": genetic_info
#     })

# # Endpoint: Predict long-term health impact
# @app.route('/predict', methods=['POST'])
# def predict_health_impact():
#     data = request.get_json()
#     participant_id = data.get("ParticipantID")

#     nhanes_info = nhanes_data[nhanes_data['ParticipantID'] == participant_id]
#     genetic_info = genetic_data[genetic_data['ParticipantID'] == participant_id]

#     if nhanes_info.empty or genetic_info.empty:
#         return jsonify({"error": "Participant data is incomplete or missing"}), 404

#     # Dummy prediction logic (to be replaced with model integration)
#     prediction = {
#         "BMI": nhanes_info.iloc[0]['BMI'] + 0.5,
#         "BloodPressure": nhanes_info.iloc[0]['BloodPressure'] - 1.0,
#         "Impact": "Positive" if genetic_info.iloc[0]['Effect'] == "Neutral" else "Negative"
#     }

#     return jsonify({"prediction": prediction})

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set global variables for data storage
nhanes_data = None
genetic_data = None

# Home route
@app.route('/')
def home():
    return "Welcome to the Nutritional Impact Predictor API!"

# Endpoint: Upload CSV files
@app.route('/upload', methods=['POST'])
def upload_files():
    global nhanes_data, genetic_data
    
    if 'nhanes_file' not in request.files or 'genetic_file' not in request.files:
        return jsonify({"error": "Both 'nhanes_file' and 'genetic_file' are required"}), 400

    nhanes_file = request.files['nhanes_file']
    genetic_file = request.files['genetic_file']

    try:
        nhanes_data = pd.read_csv(nhanes_file)
        genetic_data = pd.read_csv(genetic_file)
        return jsonify({"message": "Files uploaded and data loaded successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to read files: {str(e)}"}), 500

# Endpoint: Get all participants
@app.route('/participants', methods=['GET'])
def get_participants():
    if nhanes_data is None:
        return jsonify({"error": "Nutritional data is not uploaded yet"}), 400

    participants = nhanes_data['ParticipantID'].tolist()
    return jsonify({"participants": participants})

# Endpoint: Get participant details
@app.route('/participant/<participant_id>', methods=['GET'])
def get_participant_details(participant_id):
    if nhanes_data is None or genetic_data is None:
        return jsonify({"error": "Data is not uploaded yet"}), 400

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
    if nhanes_data is None or genetic_data is None:
        return jsonify({"error": "Data is not uploaded yet"}), 400

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
