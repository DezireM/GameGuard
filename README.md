# GameGuard 🛡️

**From suspicious-message detection to in-game security awareness.**

GameGuard is a gaming-focused cybersecurity prototype built for ForgeHacks 2026. It explores how machine learning and transparent security rules can help players recognize potential scams, with a long-term goal of bringing timely security warnings directly into supported gaming environments.

## The Problem

Gamers can encounter messages promising free skins or rewards, threatening account bans, impersonating trusted people, or asking for passwords and verification codes. Recognizing these warning signs can be difficult when players are focused on gameplay.

Many security tools require users to leave their game, copy a suspicious message, and check it separately. GameGuard explores a more convenient approach: helping players recognize risks at the moment they encounter them.

## Our Current Prototype

GameGuard currently provides two features in a web application:

1. **Gaming Message Checker:** uses a machine-learning pipeline trained on the UCI SMS Spam Collection dataset to estimate whether a message resembles spam. It also identifies selected warning signs and provides practical safety recommendations.
2. **Minecraft Server Configuration Check:** uses rule-based checks to flag selected settings in Minecraft Java Edition `server.properties`.

These features demonstrate the current approach to message analysis and security guidance. The message model was trained on general SMS data, not a representative dataset of gaming scams.

## Our Vision: In-Game Protection

The long-term goal is to evolve GameGuard into an in-game security companion that can present clear warnings during gameplay, helping players pause before interacting with suspicious messages or offers.

Instead of requiring players to open a separate website, a future integration could display a lightweight notification explaining the warning signs and suggesting a safer action.

This is a planned direction, not a feature implemented in the current prototype. Actual integration would depend on the target game's supported interfaces, permissions, and platform rules.

## Technology

- Python
- Streamlit
- scikit-learn
- TF-IDF and Logistic Regression for message classification
- Rule-based checks for Minecraft server configuration

A separate Random Forest experiment used the UCI Phishing Websites dataset. It requires webpage-derived features and is not currently integrated as a detector for arbitrary pasted URLs.

## Limitations

The message model has not been validated on a dedicated, representative gaming-scam dataset. Its output is not proof that a message is fraudulent or safe.

The server checker examines only a small number of settings. It is not a complete security audit.

GameGuard does not currently monitor gameplay, intercept in-game messages, or display live in-game security notifications.
