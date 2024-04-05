import smtplib
from email.message import EmailMessage
import ssl
from cryptography.fernet import Fernet
from db import mongo
from bson import ObjectId
class EmailSender:
    def __init__(self, smtp_server='smtp.gmail.com', port=465):
        # Retrieve the user from MongoDB
        email = mongo.db.email.find_one({'_id': ObjectId("660fec7cd3abed179b7f9b23")})

        key = '-pN6wo1i-zluULNfiXjI-PP1afYzEhdhZit_hns-6hU='
        cipher_suite = Fernet(key)

        # Decrypt the username and password
        decrypted_username = cipher_suite.decrypt(email['username']).decode()
        decrypted_password = cipher_suite.decrypt(email['password']).decode()
        print(decrypted_username)
        print(decrypted_password)
        self.smtp_server = smtp_server
        self.port = port
        self.username = decrypted_username
        self.password = decrypted_password

    def send_email(self, to_email, otp_verified):
        # Prepare the email
        em = EmailMessage()
        em.set_content('Your OTP verification was successful.' if otp_verified else 'Your OTP verification failed.')
        em['Subject'] = 'OTP Verification'
        em['From'] = self.username
        em['To'] = to_email


        # Create an insecure SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail( self.username, to_email, em.as_string())



