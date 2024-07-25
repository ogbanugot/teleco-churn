# teleco-churn
ML Task for Predicting Customer Churn for a Teleco

## Dataset
The dataset is from this Kaggle repo https://www.kaggle.com/datasets/shilongzhuang/telecom-customer-churn-by-maven-analytics

## Training Results
The notebook [Teleco-Churn-Prediction.ipynb](Teleco-Churn-Prediction.ipynb) has the main preprocessing, training and evaluation results.

## Discussion & Recommendations
XGBoost is the best performing model overall based on the metrics:

Accuracy: Highest at 83.83%  
Precision: Highest at 87.85%  
Recall: Highest at 90.56%  
F1-score: Highest at 89.18%  
AUC-ROC: Highest at 89.19%  

### Why XGBoost?
XGBoost consistently outperforms the other models across all metrics, especially in recall, which is critical in a churn prediction context where catching all possible churn cases (high recall) is crucial.
The AUC-ROC score of XGBoost is also the highest, indicating better performance in distinguishing between churned and non-churned customers.

### Recommendations
1. Model Evaluation and Validation
Further Evaluation: Although XGBoost performs best, we can validate its performance further by using techniques such as cross-validation and ensuring there is no overfitting.
Hyperparameter Tuning: We might explore hyperparameter tuning for XGBoost to potentially improve its performance even further.
2. Operational Considerations
Training Time: XGBoost can be more resource-intensive compared to Logistic Regression and Random Forest. We will need to ensure that our infrastructure can handle the computational requirements for XGBoost.  
Model Complexity: XGBoost is more complex compared to Logistic Regression and Random Forest. Ensuring that we have the necessary interpretability and explainability tools to understand and trust the model’s predictions is key.  
3. Business Implementation
Deploying XGBoost: We should use the XGBoost model for the churn prediction system and integrate it for real-time predictions.
Monitor and Update: We should continuously monitor the model's performance and update it as new data comes in or as the business environment changes.
4. Additional Strategies
Ensemble Methods: We can Consider using ensemble methods like stacking models if computational resources allow. This can potentially combine the strengths of different models to achieve even better performance.
Customer Segmentation: We should use the model's predictions to segment customers into different risk categories and tailor retention strategies accordingly.

## Model Serving & Deployment
To integrate the best model (xgboost) with existing systems, we can create a REST API that takes in customer data and returns the 
model prediction. We can then containerize this service and deploy it.  
To illustrate this I have built a simple FastAPI App and deployed it on a fly.io VM.

### Make a POST Request (To the live API) for Churn Prediction:

Note: This VM has `auto_stop` so it might take a few seconds to spin up and respond. 

```shell
curl --location 'https://telcom.fly.dev/predict' \
--header 'Content-Type: application/json' \
--data '{
  "Gender": "Male",
  "Married": "No",
  "Internet_Service": "Fiber Optic",
  "Internet_Type": "Fiber Optic",
  "Online_Security": "Yes",
  "Online_Backup": "Yes",
  "Device_Protection_Plan": "No",
  "Premium_Tech_Support": "Yes",
  "Streaming_TV": "No",
  "Streaming_Movies": "Yes",
  "Streaming_Music": "Yes",
  "Unlimited_Data": "Yes",
  "Contract": "Month-to-Month",
  "Paperless_Billing": "Yes",
  "Payment_Method": "Bank Transfer",
  "Offer": "None",
  "Phone_Service": "Yes",
  "Multiple_Lines": "No",
  "Age": 45,
  "Number_of_Dependents": 1,
  "Tenure_in_Months": 36,
  "Avg_Monthly_Long_Distance_Charges": 15.75,
  "Avg_Monthly_GB_Download": 45.5,
  "Monthly_Charge": 89.99,
  "Total_Charges": 3238.64,
  "Total_Refunds": 0.0,
  "Total_Extra_Data_Charges": 10.5,
  "Total_Long_Distance_Charges": 56.5,
  "Total_Revenue": 3299.14,
  "Zip_Code": "30301",
  "Number_of_Referrals": 4
}'
```

## Run the server (locally) with Python
First install requirements
```commandline
pip install -r requirements.txt
```

Next, provide a `.env` file with keys:
```text
MODEL_PATH='best_xgboost.joblib'
PREPROCESSOR_PATH='preprocessor_pipeline.joblib'
```

Run the dev server:
```commandline
uvicorn main:app --port 8080 --reload
```

## Deploy via Dockerfile to fly.io
Based on this https://fly.io/docs/languages-and-frameworks/dockerfile/

Create the fly app
```commandline
 fly apps create telcom
```

The launch command is optional since there is a `fly.toml` file already
```commandline
fly launch --no-deploy
```

deploy app
```commandline
fly deploy --ha=false
```

### Optional
scale the memory
```commandline
flyctl scale memory 2048 -a tlb
```
scale the vm
```commandline
fly scale vm shared-cpu-2x --vm-memory 4096 -a tlb
```

