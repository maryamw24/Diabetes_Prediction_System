from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .model import Model
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Initialize FastAPI app
app = FastAPI(title="Diabetes Prediction API")

# Initialize model
model = Model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define input data model using Pydantic
class DiabetesInput(BaseModel):
    Age: float
    Gender: int  # 0 = Female, 1 = Male
    Polyuria: int  # 0 = No, 1 = Yes
    Polydipsia: int
    sudden_weight_loss: int
    weakness: int
    Polyphagia: int
    Genital_thrush: int
    visual_blurring: int
    Itching: int
    Irritability: int
    delayed_healing: int
    partial_paresis: int
    muscle_stiffness: int
    Alopecia: int
    Obesity: int

# Prediction endpoint
@app.post("/predict", response_model=dict)
async def predict(input_data: DiabetesInput):
    try:
        # Convert Pydantic model to dict
        user_input = input_data.dict()

        # Make prediction using the model
        prediction, probability = model.predict(user_input)

        # Prepare response
        result = {
            "prediction": "Diabetic" if prediction == 1 else "Non-Diabetic",
            "probability": float(probability) if probability is not None else None
        }
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Run the app (for testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)