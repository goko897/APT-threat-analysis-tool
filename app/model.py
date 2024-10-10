import numpy as np
import pickle
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder

# Initialize label encoders for categorical columns
label_encoder = LabelEncoder()

def load_model():
    model_file_path = r'APT-threat-analysis-tool/models/sgd_model.pkl'
    print(model_file_path)
    try:
        model = joblib.load(model_file_path)
        return model
    except Exception as e:
        print(f"Joblib loading error: {e}")
        try:
            with open(model_file_path, 'rb') as model_file:
                model = pickle.load(model_file)
                return model
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

def preprocess_data(df):
    # Categorical columns that need label encoding
    categorical_columns = ['publicIP', 'FlowID', 'SrcIP', 'DstIP', 'Protocol']

    # Apply label encoding to categorical columns
    for col in categorical_columns:
        if col in df.columns:
            df[col] = label_encoder.fit_transform(df[col].astype(str))

    # Replace infinite values with NaN and then drop them
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    return df

def predict_apt(csv_file, output_csv='results/predictions.csv'):
    # Load the pre-trained model
    model = load_model()

    # Load the CSV file containing network traffic data
    df = pd.read_csv(csv_file)

    # Preprocess the data
    df = preprocess_data(df)

    # Extract relevant features from the dataframe
    features = df[['publicIP','FlowID','SrcIP','SrcPort','DstIP','DstPort','Protocol',
                   'FlowDuration','TotFwdPkts','TotBwdPkts','TotLenFwdPkts','TotLenBwdPkts',
                   'FwdPktLenMax','FwdPktLenMin','FwdPktLenMean','FwdPktLenStd','BwdPktLenMax',
                   'BwdPktLenMin','BwdPktLenMean','BwdPktLenStd','FlowByts/s','FlowPkts/s',
                   'FlowIATMean','FlowIATStd','FlowIATMax','FlowIATMin','FwdIATTot','FwdIATMean',
                   'FwdIATStd','FwdIATMax','FwdIATMin','BwdIATTot','BwdIATMean','BwdIATStd',
                   'BwdIATMax','BwdIATMin','FwdPSHFlags','BwdPSHFlags','FwdURGFlags','BwdURGFlags',
                   'FwdHeaderLen','BwdHeaderLen','FwdPkts/s','BwdPkts/s','PktLenMin','PktLenMax',
                   'PktLenMean','PktLenStd','PktLenVar','FINFlagCnt','SYNFlagCnt','RSTFlagCnt',
                   'PSHFlagCnt','ACKFlagCnt','URGFlagCnt','CWEFlagCount','ECEFlagCnt','Down/UpRatio',
                   'PktSizeAvg','FwdSegSizeAvg','BwdSegSizeAvg','FwdByts/bAvg','FwdPkts/bAvg',
                   'FwdBlkRateAvg','BwdByts/bAvg','BwdPkts/bAvg','BwdBlkRateAvg','SubflowFwdPkts',
                   'SubflowFwdByts','SubflowBwdPkts','SubflowBwdByts','InitFwdWinByts','InitBwdWinByts',
                   'FwdActDataPkts','FwdSegSizeMin','ActiveMean','ActiveStd','ActiveMax','ActiveMin',
                   'IdleMean','IdleStd','IdleMax','IdleMin']]  # Adjust this according to model requirements

    # Predict APT attacks using the model
    predictions = model.predict(features)

    # Create output DataFrame with predictions
    prediction_output = df.copy()  # Keep the original data (if needed)
    prediction_output['Predicted_Label'] = label_encoder.inverse_transform(predictions)

    # Save the prediction results to a CSV file
    prediction_output.to_csv(output_csv, index=False)
    print(f"Predictions saved to {output_csv}")

    # Analyze the prediction results and return appropriate message
    if predictions.sum() > 0:
        result_message = "APT Attack Detected"
    else:
        result_message = "No APT Attack Detected"

    return result_message, output_csv

# Example usage
if __name__ == "__main__":
    result_message, output_csv = predict_apt('path_to_your_input_file.csv')
    print(result_message)
