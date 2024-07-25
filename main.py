from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from services.ml import CustomerData, preprocess_data, get_model_and_preprocessor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
@limiter.limit("10/minute")
def predict_churn(
        request: Request,
        data: CustomerData
):
    try:
        model, preprocessor = get_model_and_preprocessor()
        # Preprocess the input data
        input_data = preprocess_data(data.dict(), preprocessor)

        # Perform prediction
        prediction = model.predict(input_data)

        # Return the result
        result = "churn" if prediction[0] == 1 else "no_churn"
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
