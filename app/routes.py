from flask import render_template, request, redirect, url_for, flash, jsonify
from app.model import predict_apt  # Import the model prediction function
from app.analysis import analyze_network  # Import the analysis function for visualizations
from app.firewall import isolate_ip  # Import function to isolate suspicious IPs (if required)
from app import app
import os
import pandas as pd

# Configuration for the uploads and static folders
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'APT-threat-analysis-tool', 'uploads')
STATIC_FOLDER = os.path.join(os.getcwd(), 'APT-threat-analysis-tool', 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Render the main page with an upload form
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file is present in the request
        if 'file' not in request.files:
            flash('No file part in the request. Please upload a valid .csv file.', 'error')
            return redirect(request.url)

        file = request.files['file']

        # Check if the user selected a file
        if file.filename == '':
            flash('No file selected. Please upload a valid .csv file.', 'error')
            return redirect(request.url)

        # Ensure the file is a CSV
        if not file.filename.endswith('.csv'):
            flash('Unsupported file type. Please upload a valid .csv file.', 'error')
            return redirect(request.url)

        try:
            # Save the uploaded CSV file
            csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(csv_filepath)

            # Step 1: Read the CSV to validate its contents
            df = pd.read_csv(csv_filepath)
            if df.empty:
                flash('The uploaded CSV file is empty. Please upload a file with data.', 'error')
                return redirect(request.url)
            
            # Check for required columns in the CSV
            required_columns = {'Label', 'SrcIP', 'DstIP', 'FlowDuration'}  # Customize this based on your model requirements
            if not required_columns.issubset(set(df.columns)):
                flash(f'The uploaded CSV must contain the following columns: {required_columns}.', 'error')
                return redirect(request.url)

        except Exception as e:
            flash(f"Error reading the uploaded CSV file: {str(e)}", 'error')
            return redirect(request.url)

        # Step 2: Predict using the pre-trained AI model and generate an output CSV
        try:
            apt_status, output_csv = predict_apt(csv_filepath)  # Call the prediction function from your model
        except Exception as e:
            flash(f"Error during model prediction: {str(e)}", 'error')
            return redirect(request.url)

        # Step 3: Generate visualizations from the prediction output CSV
        try:
            visualization_paths = analyze_network(output_csv, STATIC_FOLDER)
        except Exception as e:
            flash(f"Error during visualization generation: {str(e)}", 'error')
            return redirect(request.url)

        # Step 4: If needed, isolate suspicious IPs based on analysis results (Optional)
        suspicious_ips = df[df['Label'] != 'Normal']['SrcIP'].unique()  # Example logic to find suspicious IPs
        if len(suspicious_ips) > 0:
            try:
                for ip in suspicious_ips:
                    isolate_ip(ip)  # Call function to isolate the IP
            except Exception as e:
                flash(f"Error during IP isolation: {str(e)}", 'error')

        # Step 5: Render the result page with prediction, visualizations, and suspicious IPs
        return render_template(
            'result.html', 
            apt_status=apt_status,  # APT prediction status
            attack_distribution=visualization_paths['attack_distribution'],  # Path to the distribution chart
            top_ips=visualization_paths['top_ips'],  # Path to the top malicious IPs chart (if generated)
            flow_duration=visualization_paths['flow_duration'],  # Path to the flow duration analysis chart (if generated)
            suspicious_ips=suspicious_ips  # List of isolated IPs (if any)
        )

    return render_template('index.html')
