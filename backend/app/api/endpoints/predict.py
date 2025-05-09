from fastapi import APIRouter, Depends, HTTPException
from app.schemas.predict import PredictionInput, PredictionOutput
from app.schemas.auth import User
from app.models.diabetes_model import predict_diabetes
from app.db import log_prediction
from app.dependencies import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/", response_model=PredictionOutput)
async def predict(data: PredictionInput, user: User = Depends(get_current_user)):
    try:
        if user:
            input_data = data.dict()
            prediction, probability = predict_diabetes(input_data)

            prediction_result = "Diabetic" if prediction == 1 else "Non-Diabetic"
            log_prediction(user["id"], input_data, prediction_result, probability)

            return {"prediction": prediction_result, "probability": probability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
