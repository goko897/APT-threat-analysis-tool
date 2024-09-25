from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Import CORS
import os
from utils.file_conversion import convert_file_to_csv
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULT_FOLDER'] = 'results/'
model = joblib.load('model/model.pkl')

# Your existing routes
