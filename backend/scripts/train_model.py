import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
dataset_path = "data/diabetes_dataset.csv"
data = pd.read_csv(dataset_path)

# Define features and target
features = [
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
target = "class"

# Prepare data: Convert categorical variables to numeric
data["Gender"] = data["Gender"].map({"Male": 1, "Female": 0})
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
    data[field] = data[field].map({"Yes": 1, "No": 0})

# Convert target to numeric
data[target] = data[target].map({"Positive": 1, "Negative": 0})

# Prepare features and target
X = data[features]
y = data[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model
with open("data/trained_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to data/trained_model.pkl")
