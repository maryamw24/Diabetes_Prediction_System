from pydantic import BaseModel
from typing import Literal


class PredictionInput(BaseModel):
    Age: float
    Gender: int
    Polyuria: int
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


class PredictionOutput(BaseModel):
    prediction: Literal["Diabetic", "Non-Diabetic"]
    probability: float
