# db.py
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/chalaang_bureau"  # replace with your MongoDB URI
mongo = PyMongo(app)