def preprocess_input(input_data: dict) -> dict:
    """
    Preprocess input data to match model expectations.
    Ensures all fields are present and numeric.
    """
    processed = input_data.copy()

    # Ensure all expected fields are present
    expected_fields = [
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
    for field in expected_fields:
        if field not in processed:
            raise ValueError(f"Missing field: {field}")

    # Convert Age to float
    processed["Age"] = float(processed["Age"])

    # Ensure Gender is 1 or 0 (frontend already sends 1/0)
    if processed["Gender"] not in [0, 1]:
        raise ValueError("Gender must be 1 (Male) or 0 (Female)")
    processed["Gender"] = int(processed["Gender"])

    # Ensure boolean fields are 1 or 0 (frontend already sends 1/0)
    boolean_fields = [
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
    for field in boolean_fields:
        if processed[field] not in [0, 1]:
            raise ValueError(f"{field} must be 1 (Yes) or 0 (No)")
        processed[field] = int(processed[field])

    return processed
