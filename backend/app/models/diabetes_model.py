import pickle
import pandas as pd
from app.models.preprocessing import preprocess_input

# Load the trained model
with open("data/trained_model.pkl", "rb") as f:
    model = pickle.load(f)


def predict_diabetes(input_data: dict) -> tuple[int, float]:
    """
    Predict diabetes based on input data.
    Returns: (prediction, probability)
    """
    # Preprocess input
    processed_data = preprocess_input(input_data)

    # Convert to DataFrame for prediction
    feature_names = [
        "Age",
        "Gender",
        "Polyuria",
        "Polydipsia",
        "sudden_weight_loss",
        "weakness",
        "Polyphagia",
        "Genital_thrush",
        "visual_blurring",
        "Itching",
        "Irritability",
        "delayed_healing",
        "partial_paresis",
        "muscle_stiffness",
        "Alopecia",
        "Obesity",
    ]
    input_df = pd.DataFrame([processed_data], columns=feature_names)

    # Predict
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]  # Probability of being Diabetic
    return prediction, probability
