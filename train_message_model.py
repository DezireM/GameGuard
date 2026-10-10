
from pathlib import Path
from collections import Counter

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


data_path = Path("data/SMSSpamCollection")

messages = []
labels = []

with data_path.open(encoding="utf-8") as file:
    for line in file:
        label, message = line.rstrip("\n").split("\t", 1)
        messages.append(message)
        labels.append(label)

print("Total messages:", len(messages))
print("Class counts:", Counter(labels))


X_train, X_test, y_train, y_test = train_test_split(
    messages,
    labels,
    test_size=0.20,
    random_state=42,
    stratify=labels,
)

print("\nTraining examples:", len(X_train))
print("Testing examples:", len(X_test))


model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=2,
        ),
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
        ),
    ),
])


model.fit(X_train, y_train)


predictions = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    labels=["ham", "spam"],
    zero_division=0,
))

print("Confusion matrix (rows=true, columns=predicted)")
print("Label order: ham, spam")
print(confusion_matrix(
    y_test,
    predictions,
    labels=["ham", "spam"],
))


Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/message_model.joblib")

print("\nModel saved to models/message_model.joblib")
