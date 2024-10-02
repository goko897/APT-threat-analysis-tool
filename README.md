# APT analysis tool

# Setting Up the Virtual Environment to start application
Follow these steps to create and activate a virtual environment using **virtualenv**.

# 1. Change terminal to working directory
```bash
cd src-code
```
# 2. Install `virtualenv` (if not already installed)
First, ensure you have `virtualenv` installed globally on your system:
```bash
pip install virtualenv
```

# 3. Creating virtual environment
```bash
virtualenv env
.\env\Scripts\activate
```

# 4. Install Project Dependencies
```bash
pip install -r requirements.txt
pip install --upgrade Flask Werkzeug
pip install Flask==2.0.3 Werkzeug==2.0.3
```

# 5. Start running flask program
```bash
python app.py
```
# APT analysis tool

```
apt-detection-app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── analysis.py
│   ├── model.py
│   ├── firewall.py
│   ├── pcap_to_csv.py
│   └── templates/
│       ├── index.html
│       ├── result.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
├── models/
│   └── apt_detection_model.pkl
├── run.py
└── requirements.txt
```
