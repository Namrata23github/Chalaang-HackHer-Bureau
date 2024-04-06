from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import json
import threading

from pyod.models.auto_encoder import AutoEncoder
from sklearn.model_selection import train_test_split
from pyod.models.lof import LOF
from haversine import haversine
from sklearn.metrics import precision_score, recall_score, f1_score


from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/FraudDb"
# mongo = PyMongo(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['fraud_detection']
collection = db['fraudData']

@app.route('/')
def hello():
    return "hello"


@app.route('/detect_suspicious_activity', methods=['POST'])
def detect_suspicious_activity():
    # Get the transaction data from the request
    transaction_data = request.get_json()


    # Analyze the transaction data and identify suspicious activity
    output = check_rules(transaction_data)

    return jsonify(output)


@app.route('/createDummyData', methods=['POST'])
def create_dummy_api():
    thread = threading.Thread(target=createDummy)
    thread.start()
    return jsonify({'message': 'Training started'}), 200

def createDummy():
    data = list(collection.find({}, {'_id': 0}))

    # Create 1000 new documents
    for i in range(1000):

        new_document = data[i % len(data)]
        new_document['_id'] = i
        collection.insert_one(new_document)



@app.route('/train_model', methods=['POST'])
def train_model_api():
    thread = threading.Thread(target=train_model)
    thread.start()
    return jsonify({'message': 'Training started'}), 200


def train_model():

    # Extract data from MongoDB
    transaction_data = list(collection.find({}, {'_id': 0}))
    df = pd.DataFrame(transaction_data)
    # Convert the input data to a pandas DataFrame


    df = pd.DataFrame(transaction_data)

    columns_to_keep = ['dateTimeTransaction', 'dateLocalTransaction', 'timeLocalTransaction', 'transactionAmount' , 'cardBalance', 'latitude', ]  # replace with your column names

# Preprocess the data
    df['dateTimeTransaction'] = pd.to_datetime(df['dateTimeTransaction'], format='%Y%m%d%H%M%S', errors='coerce')
    df['dateLocalTransaction'] = pd.to_datetime(df['dateLocalTransaction'], format='%y%m%d', errors='coerce')
    df['timeLocalTransaction'] = pd.to_datetime(df['timeLocalTransaction'], format='%H%M%S', errors='coerce')
    df['transactionAmount'] = df['transactionAmount'].astype(float)
    df['cardBalance'] = df['cardBalance'].astype(float)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    scaler = StandardScaler()
    numerical_cols = ['transactionAmount', 'cardBalance']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    categorical_cols = ['merchantCategoryCode', 'posEntryMode', 'network', 'transactionOrigin', 'transactionType']
    df = pd.get_dummies(df, columns=categorical_cols)

    # Split data into training and testing sets
    X = df.drop(['authorisationStatus', 'latitude', 'longitude'], axis=1)
    y = df['authorisationStatus']
    print("+++++++")
    print(X)
    print(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Import required models
    models = [
        IsolationForest(),
        AutoEncoder(hidden_neurons=[64, 32, 32, 64]),
        LOF()
    ]

    # Train and evaluate models
    for model in models:
        model.fit(X_train)
        train_scores = model.decision_function(X_train)
        test_scores = model.decision_function(X_test)

    # Evaluate model performance
    # ... (code for evaluating model performance using appropriate metrics) Below is Code

    # Train and evaluate models

    model_metrics = {}
    for model_name, model in zip(['IsolationForest', 'AutoEncoder', 'LOF'], models):
        model.fit(X_train)
        train_scores = model.decision_function(X_train)
        test_scores = model.decision_function(X_test)

    # Evaluate model performance
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    train_precision = precision_score(y_train, y_train_pred)
    train_recall = recall_score(y_train, y_train_pred)
    train_f1 = f1_score(y_train, y_train_pred)

    test_precision = precision_score(y_test, y_test_pred)
    test_recall = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)

    model_metrics[model_name] = {
        'train_precision': train_precision,
        'train_recall': train_recall,
        'train_f1': train_f1,
        'test_precision': test_precision,
        'test_recall': test_recall,
        'test_f1': test_f1
    }

    print(f"{model_name} Performance:")
    print(f"Train Precision: {train_precision:.4f}, Recall: {train_recall:.4f}, F1-Score: {train_f1:.4f}")
    print(f"Test Precision: {test_precision:.4f}, Recall: {test_recall:.4f}, F1-Score: {test_f1:.4f}")
    print("-" * 30)


    # Select best performing model
    #best_model = ...  # Code to select the best performing model based on evaluation metrics
    # Select best performing model
    best_model_name = max(model_metrics, key=lambda x: model_metrics[x]['test_f1'])
    best_model = [m for m, name in zip(models, ['IsolationForest', 'AutoEncoder', 'LOF']) if name == best_model_name][0]
    print(f"\nBest Performing Model: {best_model_name}")

    #...............Code here.........

    # Rule-based fraud detection
def check_rules(row):
    status = "OK"
    rule_violated = []

    # Rule 1
    if row['transactionAmount'] >= 0.7 * row['cardBalance'] and row['cardBalance'] >= 300000:
        trans_12h = df[(df['dateTimeTransaction'] >= row['dateTimeTransaction'] - timedelta(hours=12)) &
                       (df['dateTimeTransaction'] <= row['dateTimeTransaction']) &
                       (df['encryptedHexCardNo'] == row['encryptedHexCardNo'])]
        total_amount_12h = trans_12h['transactionAmount'].sum()
        if total_amount_12h >= 0.7 * row['cardBalance']:
            status = "ALERT"
            rule_violated.append("RULE-001")

    # Rule 2
    trans_12h = df[(df['dateTimeTransaction'] >= row['dateTimeTransaction'] - timedelta(hours=12)) &
                   (df['dateTimeTransaction'] <= row['dateTimeTransaction']) &
                   (df['encryptedHexCardNo'] == row['encryptedHexCardNo'])]
    locations = trans_12h[['latitude', 'longitude']].drop_duplicates()
    if len(locations) > 5:
        total_amount_12h = trans_12h['transactionAmount'].sum()
        if total_amount_12h > 100000:
            for i in range(len(locations)-1):
                for j in range(i+1, len(locations)):
                    distance = haversine((locations.iloc[i]['latitude'], locations.iloc[i]['longitude']),
                                         (locations.iloc[j]['latitude'], locations.iloc[j]['longitude']))
                    if distance >= 200:
                        status = "ALERT"
                        rule_violated.append("RULE-002")
                        break
                if "RULE-002" in rule_violated:
                    break

    # Rule 3
    # Check for coherent pattern based on historical data
    window_sizes = [12, 24, 168]  # 12 hours, 1 day, 7 days
    for window_size in window_sizes:
        historical_trans = df[(df['dateTimeTransaction'] >= row['dateTimeTransaction'] - timedelta(hours=window_size)) &
                              (df['dateTimeTransaction'] < row['dateTimeTransaction']) &
                              (df['encryptedHexCardNo'] == row['encryptedHexCardNo'])]
        if not check_coherent_pattern(historical_trans, row):
            status = "ALERT"
            rule_violated.append("RULE-003")
            break

    # Rule 4
    # Check for coherent pattern based on merchant category code
    window_sizes = [72, 168, 720]  # 3 days, 7 days, 30 days
    for window_size in window_sizes:
        historical_trans = df[(df['dateTimeTransaction'] >= row['dateTimeTransaction'] - timedelta(hours=window_size)) &
                              (df['dateTimeTransaction'] < row['dateTimeTransaction']) &
                              (df['encryptedHexCardNo'] == row['encryptedHexCardNo'])]
        if not check_merchant_pattern(historical_trans, row):
            status = "ALERT"
            rule_violated.append("RULE-004")
            break

    return {
        "status": status,
        "ruleViolated": rule_violated,
        "timestamp": str(int(datetime.now().timestamp()))
    }
# Helper functions
def check_coherent_pattern(historical_trans, current_trans):
    # ... (code to check for coherent pattern based on historical data)
    # Replace with actual logic

    mean_amount = historical_trans['transactionAmount'].mean()
    std_amount = historical_trans['transactionAmount'].std()

    # Check if the current transaction amount is within 2 standard deviations of the historical mean
    if abs(current_trans['transactionAmount'] - mean_amount) <= 2 * std_amount:
        return True
    else:
        return False

def check_merchant_pattern(historical_trans, current_trans):
    # ... (code to check for coherent pattern based on merchant category code)
    # Replace with actual logic
    mode_mcc = historical_trans['merchantCategoryCode'].mode().iloc[0]

    # Check if the current transaction has the same merchant category code as the most common one
    if current_trans['merchantCategoryCode'] == mode_mcc:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)