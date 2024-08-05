from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Enable CORS for specific origin

# Load and preprocess the dataset
try:
    df = pd.read_csv('new_data.csv')
    df['race_id'] = df['race_id'].astype(str)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')  # Standardize date format
    print(f"Dataset loaded successfully. Number of rows: {len(df)}")
    print(f"Dataset sample:\n{df.head()}")  # Print sample data for verification
except Exception as e:
    print(f"Error loading dataset: {e}")

# Load the trained model
try:
    model = joblib.load('horse_racing_model.joblib')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Define the feature columns
feature_columns = ['behind_sec3', 'win_odds', 'position_sec1', 'position_sec2', 'position_sec3', 'result', 'horse_no']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_race_ids', methods=['POST'])
def get_race_ids():
    try:
        selected_date = request.json['date']
        print(f"Received date: {selected_date}")  # Debugging log
        
        # Convert selected_date to match the standardized date format
        selected_date = pd.to_datetime(selected_date).strftime('%Y-%m-%d')
        print(f"Standardized date: {selected_date}")

        # Log the unique dates in the dataset for comparison
        unique_dates = df['date'].unique()
        print(f"Unique dates in dataset: {unique_dates}")
        
        race_ids_on_date = df[df['date'] == selected_date]['race_id'].unique()
        print(f"Race IDs on date {selected_date}: {race_ids_on_date}")  # Debugging log
        
        race_ids_on_date_list = race_ids_on_date.tolist()
        if len(race_ids_on_date_list) == 0:
            print(f"No race IDs found for date: {selected_date}")
            return jsonify({'error': 'No race IDs found for the selected date.'}), 404

        return jsonify({'race_ids': race_ids_on_date_list})
    except Exception as e:
        print(f"Error fetching race IDs: {e}")  # Debugging log
        return jsonify({'error': 'Error fetching race IDs.'}), 500

@app.route('/predict', methods=['POST'])
def predict_winner():
    try:
        selected_race_id = request.json['race_id']
        print(f"Received race ID: {selected_race_id}")  # Debugging log
        
        race_data = df[df['race_id'] == selected_race_id][feature_columns]
        if race_data.empty:
            print(f"Race ID {selected_race_id} not found in the dataset.")
            return jsonify({'error': 'Race ID not found.'}), 404
        
        print(f"Race data for race ID {selected_race_id}: {race_data}")  # Debugging log
        
        race_probabilities = model.predict_proba(race_data)
        print(f"Race probabilities: {race_probabilities}")  # Debugging log
        
        winning_probabilities = race_probabilities[:, 1]
        winning_horse_index = winning_probabilities.argmax()
        winning_horse_number = race_data.iloc[winning_horse_index]['horse_no']
        winning_percentage = winning_probabilities[winning_horse_index] * 100
        
        return jsonify({'winner_horse_number': winning_horse_number, 'winning_percentage': winning_percentage})
    except Exception as e:
        print(f"Error predicting winner: {e}")  # Debugging log
        return jsonify({'error': 'Error predicting winner.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
