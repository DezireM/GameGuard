
import joblib

model = joblib.load("models/message_model.joblib")

test_cases = [
    (
        "SCAM",
        "Claim your free game skins now. Enter your password to receive them.",
    ),
    (
        "SCAM",
        "Your account will be permanently banned. Verify your login immediately.",
    ),
    (
        "SCAM",
        "I am a game moderator. Send me your verification code to restore your account.",
    ),
    (
        "NORMAL",
        "Are you joining our Minecraft server tonight?",
    ),
    (
        "NORMAL",
        "Good game everyone. Let's play again tomorrow.",
    ),
    (
        "SECURITY ALERT",
        "A login was detected on your account from a new device.",
    ),
]

print("GAMEGUARD: GAMING MESSAGE TEST")
print("=" * 55)

for category, message in test_cases:
    probabilities = model.predict_proba([message])[0]
    classes = list(model.classes_)
    spam_probability = probabilities[classes.index("spam")]
    prediction = model.predict([message])[0]

    print(f"\nExample type: {category}")
    print(f"Message: {message}")
    print(f"Model prediction: {prediction}")
    print(f"Spam probability: {spam_probability:.1%}")
