import joblib
import pandas as pd
import numpy as np
from typing import Tuple
class Model:
    def __init__(self):
        try:
            self.model = joblib.load('backend/models/random_forest_model.pkl')
        except FileNotFoundError:
            raise Exception("Model or scaler file not found. Please train the model first.")

        # Define feature columns (matching the dataset)
        self.feature_columns = [
            'Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden_weight_loss', 'weakness',
            'Polyphagia', 'Genital_thrush', 'visual_blurring', 'Itching', 'Irritability',
            'delayed_healing', 'partial_paresis', 'muscle_stiffness', 'Alopecia', 'Obesity'
        ]

    def predict(self, user_input: dict) -> Tuple[int, float]:
        """
        Make a diabetes prediction based on user input.

        Args:
            user_input (dict): Dictionary containing feature values (e.g., Age, Gender, etc.).

        Returns:
            Tuple[int, float]: Prediction (0 or 1) and probability of diabetes (if available).

        Raises:
            ValueError: If input data is invalid.
        """
        # Convert user input to DataFrame
        input_df = pd.DataFrame([user_input], columns=self.feature_columns)

        # Debug: Log input (in production, use proper logging)
        for col in input_df.columns:
            print(f"Input {col}: {input_df[col].values[0]}")

        # Validate numerical inputs
        if user_input['Age'] <= 0:
            raise ValueError("Age must be positive")

        # Validate categorical/binary columns
        categorical_cols = [
            'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss', 'weakness',
            'Polyphagia', 'Genital thrush', 'visual blurring', 'Itching', 'Irritability',
            'delayed healing', 'partial paresis', 'muscle stiffness', 'Alopecia', 'Obesity'
        ]
        for col in categorical_cols:
            if col in input_df.columns:
                input_df[col] = input_df[col].astype(int)
                if not input_df[col].isin([0, 1]).all():
                    raise ValueError(f"Column {col} must be 0 or 1")

        # Make prediction
        prediction = self.model.predict(input_df)
        probability = self.model.predict_proba(input_df)[:, 1] if hasattr(self.model, 'predict_proba') else None

        return prediction[0], probability[0] if probability is not None else None