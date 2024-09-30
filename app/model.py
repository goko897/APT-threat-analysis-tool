import pickle
import pandas as pd

def load_model():
    with open('models/apt_detection_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_apt(csv_file):
    model = load_model()
    df = pd.read_csv(csv_file)
    features = df[['src_ip', 'dst_ip', 'protocol', 'length']]  # Modify based on model input requirements
    prediction = model.predict(features)
    
    if prediction.sum() > 0:
        return "APT Attack Detected"
    else:
        return "No APT Attack Detected"
