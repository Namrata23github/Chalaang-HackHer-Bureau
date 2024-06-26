from datetime import datetime, timedelta
from utils import  calculate_distance
import numpy as np
from model.arima import predict
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.preprocessing import StandardScaler


def rule_1( data):
    print("rule 1")
    transaction_amount = float(data['transactionAmount'])
    card_balance = float(data['cardBalance'])

    # Check the rule
    if transaction_amount >= 0.7 * card_balance and card_balance >= 300000:
        return "ALERT", "RULE-001"
    else:
        return "OK", None

def rule_2( data):
    print("rule 2")
    transactions = pd.read_csv('dataset/synthetic_data_rule.csv', on_bad_lines='warn')
    locations = [(float(data["latitude"]), float(data["longitude"]))]
    total_amount = float(data["transactionAmount"])
    start_time = datetime.strptime(data["dateTimeTransaction"], '%d%m%y%H%M')
    end_time = start_time + timedelta(hours=12)

    for index, trans in transactions.iterrows():
        trans_time = datetime.fromtimestamp(trans["dateTimeTransaction"])
        if start_time <= trans_time <= end_time:
            total_amount += float(trans["transactionAmount"])
            for loc in locations:
                if calculate_distance(float(trans["latitude"]), float(trans["longitude"]), loc[0], loc[1]) >= 200:
                    locations.append((float(trans["latitude"]), float(trans["longitude"])))

    if len(locations) > 5 and total_amount > 100000:
        return "ALERT", "RULE-002"
    else:
        return "OK", None

def prepare_data_rule3(row):
    transactions = pd.read_csv('dataset/synthetic_data_rule.csv', on_bad_lines='warn')
    row_df = pd.json_normalize(row)

    # Create a copy of transactions before converting 'dateTimeTransaction' to timestamp
    transactions_copy = transactions.copy()

    row_df['dateTimeTransaction'] = row_df['dateTimeTransaction'].apply(lambda x: datetime.strptime(x, '%d%m%y%H%M').timestamp())
    data = []

    # Append row to transactions
    transactions = pd.concat([transactions, row_df], ignore_index=True)

    for _, transaction in transactions.iterrows():
        encoder = OneHotEncoder()
        one_hot = encoder.fit_transform(np.array(transaction['channel']).reshape(-1, 1))

        # Use the original 'dateTimeTransaction' from transactions_copy
        timestamp = pd.to_datetime(transaction['dateTimeTransaction']).timestamp()
        # Convert csr_matrix to numpy array and flatten it
        one_hot_array = one_hot.toarray().flatten()

        # Convert boolean values to integer
        preValidated = int(transaction['preValidated'])
        enhancedLimitWhiteListing = int(transaction['enhancedLimitWhiteListing'])
        isExternalAuth = int(transaction['isExternalAuth'])
        isTokenized = int(transaction['isTokenized'])
        moneySendTxn = int(transaction['moneySendTxn'])
        authorisationStatus = int(transaction['authorisationStatus'])

        # Extract numerical features from the transaction
        features = [
            int(transaction['processingCode']),
            float(transaction['transactionAmount']),
            timestamp,
            int(transaction['posEntryMode']),
            float(transaction['cardBalance']),
            preValidated,
            enhancedLimitWhiteListing,
            isExternalAuth,
            isTokenized,
            moneySendTxn,
            authorisationStatus,
            *one_hot_array,  # use the * operator to unpack the array
        ]
        data.append(features)
    # Normalize data
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    return np.array(data)

def prepare_data_rule4(row):
    data = []

    transactions = pd.read_csv('dataset/synthetic_data_rule.csv', on_bad_lines='warn')
    row_df = pd.json_normalize(row)

    # Append row to transactions
    transactions = pd.concat([transactions, row_df], ignore_index=True)

    for _, transaction in transactions.iterrows():

        # Extract numerical features from the transaction
        features = [
            int(transaction['merchantCategoryCode']),
        ]
        data.append(features)
    # Normalize data
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    return np.array(data)

def rule_3( row):
    print("rule 3")
    data = prepare_data_rule3(row)
    predict_data = data[-1]
    # Get the current time
    now = datetime.now()
    time_12_hours_ago = now - timedelta(hours=12)

    transactions_12h = data[data[:, 2] >= time_12_hours_ago.timestamp()]

    # Convert numpy array to DataFrame
    transactions_12h_df = pd.DataFrame(transactions_12h)

    if ( len(transactions_12h) > 0):
        predict_data_df = pd.DataFrame(predict_data.reshape(1, -1))
        transactions_12h = pd.concat([transactions_12h_df, predict_data_df], ignore_index=True)
        y_pred = predict(transactions_12h, len(transactions_12h))
        if y_pred[0] == -1:
            return "ALERT", "RULE-003"

    time_24_hours_ago = now - timedelta(hours=24)

    transactions_24h = data[data[:, 2] >= time_24_hours_ago.timestamp()]

    # Convert numpy array to DataFrame
    transactions_24h_df = pd.DataFrame(transactions_24h)

    if ( len(transactions_24h) > 0):
        predict_data_df = pd.DataFrame(predict_data.reshape(1, -1))
        transactions_24h = pd.concat([transactions_24h_df, predict_data_df], ignore_index=True)
        y_pred = predict(transactions_24h, len(transactions_24h))
        if y_pred[0] == -1:
            return "ALERT", "RULE-003"

        # Get the current time
    time_7_days_ago = now - timedelta(days=7)

    transactions_7d = data[data[:, 2] >= time_7_days_ago.timestamp()]

    # Convert numpy array to DataFrame
    transactions_7d_df = pd.DataFrame(transactions_7d)

    if ( len(transactions_7d) > 0):
        predict_data_df = pd.DataFrame(predict_data.reshape(1, -1))
        transactions_7d = pd.concat([transactions_7d_df, predict_data_df], ignore_index=True)
        y_pred = predict(transactions_7d, len(transactions_7d))
        if y_pred[0] == -1:
            return "ALERT", "RULE-003"

    return "OK", None




def rule_4( row):
    print("rule 4")
    data = prepare_data_rule4(row)
    y_pred = predict(data)
    if y_pred[0] == -1:
        return "ALERT", "RULE-004"
    else:
        return "OK", None



def check_rules(row):
    rule_violated = []
    rules = [rule_1, rule_2, rule_3, rule_4]
    status = "OK"
    for rule in rules:
        status, rule_id = rule( row)
        print(status, rule_id)
        if status == "ALERT":
            rule_violated.append(rule_id)
            status = "ALERT"
    return {
        "status": "OK" if len(rule_violated) == 0 else "ALERT",
        "ruleViolated": rule_violated,
        "timestamp": str(int(datetime.now().timestamp()))
    }