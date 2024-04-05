# app.py
from flask import Flask
from db import mongo
from flask import request, jsonify
from run_model import make_prediction
from user import user_bp
from email_sender import EmailSender


app = Flask(__name__)
app.register_blueprint(user_bp)  # Register the blueprint
email_sender = EmailSender()


@app.route('/api/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Extract the email and otpVerified fields
    email = data.get('emailId')
    otp_verified = data.get('otpVerfied')

    # Validate the data
    if not email or otp_verified is None:
        return jsonify({'error': 'Missing required parameter'}), 400

    # Send the email
    email_sender.send_email(email, otp_verified)

    return jsonify({'message': 'Email sent successfully.'}), 200

@app.route('/find')
def find_document():
    document = mongo.db.transactions.find_one()  # replace 'collection' with your collection name
    return str(document)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the request body
   # data = request.get_json()

    # Ensure data is in the correct format and transform if necessary
    # This step will depend on how your model expects the data

    # Make a prediction
    prediction = make_prediction()

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)