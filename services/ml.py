import os
import joblib
import pandas as pd
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

# Load XGBoost model
model_path = os.getenv("MODEL_PATH")
preprocessor_path = os.getenv("PREPROCESSOR_PATH")
model = joblib.load(model_path)
preprocessor = joblib.load(preprocessor_path)


def get_model_and_preprocessor():
    return model, preprocessor


class CustomerData(BaseModel):
    # Categorical features
    Gender: str
    Married: str
    Internet_Service: str
    Internet_Type: str
    Online_Security: str
    Online_Backup: str
    Device_Protection_Plan: str
    Premium_Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Streaming_Music: str
    Unlimited_Data: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Offer: str
    Phone_Service: str
    Multiple_Lines: str

    # Numerical features
    Age: int
    Number_of_Dependents: int
    Tenure_in_Months: int
    Avg_Monthly_Long_Distance_Charges: float
    Avg_Monthly_GB_Download: float
    Monthly_Charge: float
    Total_Charges: float
    Total_Refunds: float
    Total_Extra_Data_Charges: float
    Total_Long_Distance_Charges: float
    Total_Revenue: float
    Zip_Code: str
    Number_of_Referrals: int


def preprocess_data(data: dict, preprocessor) -> pd.DataFrame:
    # Convert the single example to a DataFrame
    new_data_df = pd.DataFrame([data])

    # Calculate engineered features for the single example
    new_data_df['CLTV'] = new_data_df['Total_Revenue'] - new_data_df['Total_Refunds']
    new_data_df['ARPU'] = new_data_df['Total_Revenue'] / new_data_df['Tenure_in_Months']
    new_data_df['LongDistanceChargeRatio'] = new_data_df['Avg_Monthly_Long_Distance_Charges'] / new_data_df[
        'Monthly_Charge']

    # Apply the preprocessing pipeline to the single example
    single = preprocessor.transform(new_data_df)
    return single
