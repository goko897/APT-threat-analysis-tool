from flask import render_template, request, redirect, url_for
from app import app
from app.pcap_to_csv import convert_pcap_to_csv
from app.model import predict_apt
from app.analysis import analyze_network
from app.firewall import isolate_ip
import os

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Convert pcap to CSV
        csv_file = convert_pcap_to_csv(filepath)
        
        # Predict using AI model
        apt_status = predict_apt(csv_file)
        
        # Analyze network activities
        analysis_result = analyze_network(csv_file)
        
        # Isolate infected IP addresses
        suspicious_ips = analysis_result['suspicious_ips']
        for ip in suspicious_ips:
            isolate_ip(ip)
        
        return render_template('result.html', apt_status=apt_status, analysis=analysis_result)
