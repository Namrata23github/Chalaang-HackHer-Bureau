from datetime import datetime, timedelta
from utils import  calculate_distance
import numpy as np
from model.arima import predict
from sklearn.preprocessing import OneHotEncoder


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
    locations = [(float(data["latitude"]), float(data["longitude"]))]
    total_amount = float(data["transactionAmount"])
    start_time = datetime.strptime(data["dateTimeTransaction"], '%d%m%y%H%M')
    end_time = start_time + timedelta(hours=12)

    # for trans in transactions:
    #     trans_time = datetime.strptime(trans["dateTimeTransaction"], '%d%m%y%H%M')
    #     if start_time <= trans_time <= end_time:
    #         total_amount += float(trans["transactionAmount"])
    #         for loc in locations:
    #             if calculate_distance(float(trans["latitude"]), float(trans["longitude"]), loc[0], loc[1]) >= 200:
    #                 locations.append((float(trans["latitude"]), float(trans["longitude"])))

    if len(locations) > 5 and total_amount > 100000:
        return "ALERT", "RULE-002"
    else:
        return "OK", None

def prepare_data(transaction):
    data = []
    encoder = OneHotEncoder()
    one_hot = encoder.fit_transform(np.array(transaction['channel']).reshape(-1, 1))

# Extract numerical features from the transaction
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
        int(transaction['dateTimeTransaction']),
        int(transaction['merchantCategoryCode']),
        int(transaction['posEntryMode']),
        float(transaction['cardBalance']),
        preValidated,
        enhancedLimitWhiteListing,
        isExternalAuth,
        isTokenized,
        moneySendTxn,
        authorisationStatus,
        one_hot,
        float(transaction['latitude']),
        float(transaction['longitude'])
    ]

    data.append(features)
    return np.array(data)

def rule_3( row):
    print("rule 3")
    data = prepare_data(row)
    y_pred = predict(data)
    if y_pred[0] == -1:
        return "ALERT", "RULE-003"
    else:
        return "OK", None



def rule_4( row):
    print("rule 4")
    d = 0



def check_rules(row):
    rule_violated = []
    rules = [rule_1, rule_2, rule_3, rule_4]
    status = "OK"
    for rule in rules:
        status, rule_id = rule( row)
        if status == "ALERT":
            rule_violated.append(rule_id)
            status = "ALERT"
    return {
        "status": status,
        "ruleViolated": rule_violated,
        "timestamp": str(int(datetime.now().timestamp()))
    }