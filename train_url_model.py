
from pathlib import Path

import joblib
import pandas as pd
from scipy.io import arff
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

data_path = Path("data/url/Training Dataset.arff")
raw_data, metadata = arff.loadarff(data_path)

df = pd.DataFrame(raw_data)
df.columns = [column.strip() for column in df.columns]

print("Dataset shape:", df.shape)
print("\nTarget label counts:")
print(df["Result"].value_counts())

X = df.drop(columns=["Result"]).astype(int)
y = df["Result"].astype(int)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining examples:", len(X_train))
print("Testing examples:", len(X_test))

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

print("Confusion matrix (rows=true, columns=predicted):")
print("Label order:", list(model.classes_))
print(confusion_matrix(y_test, predictions, labels=model.classes_))

Path("models").mkdir(exist_ok=True)

joblib.dump(
    {"model": model, "feature_names": list(X.columns)},
    "models/url_model.joblib",
)

print("\nModel saved to models/url_model.joblib")
