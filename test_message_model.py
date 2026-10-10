
import joblib

model = joblib.load("models/message_model.joblib")

print("GameGuard Message Detector")
print("Type a message to check it.")
print("Type 'quit' to exit.\n")

while True:
    message = input("Enter message: ")

    if message.lower() == "quit":
        print("Goodbye!")
        break

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]
    classes = list(model.classes_)
    spam_probability = probabilities[classes.index("spam")]

    if prediction == "spam":
        print(f"⚠️ Suspicious message (spam probability: {spam_probability:.1%})")
    else:
        print(f"Message classified as legitimate (spam probability: {spam_probability:.1%})")

    print()
