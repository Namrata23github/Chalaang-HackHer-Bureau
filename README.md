![image](https://github.com/Namrata23github/Chalaang-HackHer-Bureau/assets/55127886/8af6bc9d-e47c-4754-84cf-9bd39fb0fd0c)![image](https://github.com/Namrata23github/Chalaang-HackHer-Bureau/assets/55127886/81bfaf7d-0168-4fe4-a63b-e3f2bd664ea3)![image](https://github.com/Namrata23github/Chalaang-HackHer-Bureau/assets/55127886/88cabceb-89c8-4bb5-b36b-2c1508045164)# Chalaang-HackHer-Bureau


Theme: Develop an API that uses machine learning to analyse payment transactions and identify suspicious activity in real-time.

Building a Real-Time Fraud Detection API to detect and curtail frauds

The solution flags these scenarios:

1. If the user tries to make transactions with a total cumulative amount >= to 70% of the card balance and the balance >= Rs 3,00,000 within 12 hours. (RULE-001)
   Logic: Mathematical logic
2. Users transact from more than 5 locations (the minimum difference is 200KM between two locations) and transact with that card for more than 1,00,000 Rs within a 12-hour window. (RULE-002)
   Logic: Mathematical logic
3. If the transactions from a card don’t follow the coherent pattern of the last 12-hour/1-day/7-day window. (RULE-003)
   Logic: ARIMA model/Autoencoder model
4. If the transaction doesn’t follow a coherent pattern with the merchant category code of the last 3-day/7-day/30-day for the card (RULE-004)
   Logic: ARIMA model on merchant category code


   
## The input is a json payload containing relevant fields is in following format:

{
"mti": "0100",
"processingCode": "000000",
"transactionAmount": "0000000000.00",
"dateTimeTransaction": "2412192200",
"cardholderBillingConversionRate": "61000000",
"stan": "13244",
"timeLocalTransaction": "192200",
"dateLocalTransaction": "2412",
"expiryDate": "2306",
"conversionDate": "0911",
"merchantCategoryCode": "5969",
"posEntryMode": "810",
"acquiringInstitutionCode": "013992",
"forwardingInstitutionCode": "001695",
"rrn": "1122033441",
"cardAcceptorTerminalId": "8999840",
"cardAcceptorId": "89050840 ",
"cardAcceptorNameLocation": "NETFLIXUS",
"cardBalance": "0000000000.00",
"additionalData48": "T",
"transactionCurrencyCode": "840",
"cardholderBillingCurrencyCode": "840",
"posDataCode": "102510800600084063368",
"originalDataElement": "01001324424121922000000001399200000001695", "channel": "ECOM",
"encryptedPan": "Kg1WR6lwTruEPIDK0GS4w82/wrFeXTU5SjD9TfyUXmc=", "network": "MASTER",
"dcc": false,
"kitNo": "1020001031",
"factorOfAuthorization": 0,
"authenticationScore": 0,
"contactless": false,
"international": true,
"preValidated": false,
"enhancedLimitWhiteListing": false,
"transactionOrigin": "ECOM",
"transactionType": "ECOM",
"isExternalAuth": false,
"encryptedHexCardNo":"2a0d5647a9704ebb843c80cad064b8c3cdbfc2b15e5d35394a30fd4dfc945e67",
"isTokenized": false,
"entityId": "EKCZSH8MA5",
"moneySendTxn": false,
"mcRefundTxn": false,
"mpqrtxn": false,
"authorisationStatus": true,
"latitude": "28.644800",
"longitude":"77.216721"
}

## The output response is in json and in this structure: 

{

"status": "ALERT/OK",
"ruleViolated": ["RULE-001", "RULE-003"],
"timestamp": "unix timestamp in string"

}


## Usage: 

Use postman or any other api tester tools

OR

curl --location 'http://127.0.0.1:5000/detect_suspicious_activity' \
--header 'Content-Type: application/json' \
--data '{
"mti": "0100",
"processingCode": "000000",
"transactionAmount": "0000000000.00",
"dateTimeTransaction": "2412192200",
"cardholderBillingConversionRate": "61000000",
"stan": "13244",
"timeLocalTransaction": "192200",
"dateLocalTransaction": "2412",
"expiryDate": "2306",
"conversionDate": "0911",
"merchantCategoryCode": "5969",
"posEntryMode": "810",
"acquiringInstitutionCode": "013992",
"forwardingInstitutionCode": "001695",
"rrn": "1122033441",
"cardAcceptorTerminalId": "8999840",
"cardAcceptorId": "89050840 ",
"cardAcceptorNameLocation": "NETFLIXUS",
"cardBalance": "0000000000.00",
"additionalData48": "T",
"transactionCurrencyCode": "840",
"cardholderBillingCurrencyCode": "840",
"posDataCode": "102510800600084063368",
"originalDataElement": "01001324424121922000000001399200000001695", "channel": "ECOM",
"encryptedPan": "Kg1WR6lwTruEPIDK0GS4w82/wrFeXTU5SjD9TfyUXmc=", "network": "MASTER",
"dcc": false,
"kitNo": "1020001031",
"factorOfAuthorization": 0,
"authenticationScore": 0,
"contactless": false,
"international": true,
"preValidated": false,

"enhancedLimitWhiteListing": false, "transactionOrigin": "ECOM", "transactionType": "ECOM", "isExternalAuth": false, "encryptedHexCardNo":

"2a0d5647a9704ebb843c80cad064b8c3cdbfc2b15e5d35394a30fd4dfc945e67", "isTokenized": false,
"entityId": "EKCZSH8MA5",
"moneySendTxn": false,

"mcRefundTxn": false, "mpqrtxn": false, "authorisationStatus": true, "latitude": "28.644800", "longitude":"77.216721"

}'



## More about autoencoder:

Features used:

"processingCode","transactionAmount","dateTimeTransaction","merchantCategoryCode","posEntryMode","cardBalance","channel","factorOfAuthorization","authenticationScore","preValidated","enhancedLimitWhiteListing","isExternalAuth", "isTokenized", "moneySendTxn", "authorisationStatus", "latitude", "longitude“
   
Architecture: 

Input Layer: This defines the shape of the input data. The shape=(input_dim,) specifies that the input data is a one-dimensional array with input_dim elements.
Encoder:
The first Dense layer with 64 units and ReLU activation function (activation='relu') compresses the input data into a 64-dimensional representation.
The second Dense layer with 32 units further compresses the data into a 32-dimensional representation.
The third Dense layer with 16 units further compresses the data into a 16-dimensional representation.
Decoder:
The first Dense layer with 32 units and ReLU activation function (activation='relu') decompresses the 16-dimensional representation into a 32-dimensional representation.
The second Dense layer with 64 units further decompresses the data into a 64-dimensional representation.
The last Dense layer with input_dim units and sigmoid activation (activation='sigmoid') aims to reconstruct the original input. Sigmoid activation is commonly used for binary data (output values between 0 and 1), while linear activation is more appropriate for continuous data.
Model:
This code snippet defines the autoencoder model using the Keras functional API.
The Input layer defines the input shape.
The subsequent layers define the encoder and decoder as described above.
The Model class is then used to define the full autoencoder model, specifying the input and output layers.
Overall, this architecture is a basic autoencoder with three encoding layers and three decoding layers, where the input data is progressively compressed and then decompressed to reconstruct the original input. The choice of activation functions (ReLU for encoding layers and sigmoid for decoding the final layer) and layer sizes can be adjusted based on the specific problem and data characteristics.


