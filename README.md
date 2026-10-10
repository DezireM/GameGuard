# GameGuard 🛡️

**A gaming-focused cybersecurity prototype for ForgeHacks 2026**

## The Problem

Gamers can encounter suspicious messages promising free skins, threatening account bans, or asking for passwords and verification codes. Minecraft server operators also need to review important configuration settings.

## Our Solution

GameGuard combines two prototype features in one interface:

1. **Gaming Message Checker:** uses a machine-learning pipeline trained on the UCI SMS Spam Collection dataset to estimate whether a message resembles spam.
2. **Minecraft Server Configuration Check:** uses rule-based checks to flag selected settings in Minecraft Java Edition `server.properties`.

## Technology

- Python
- Streamlit
- scikit-learn
- TF-IDF and Logistic Regression for message classification
- Rule-based configuration checks for Minecraft server settings

A separate Random Forest experiment was trained using the UCI Phishing Websites dataset. It requires the dataset's webpage features, so it is not currently presented as a detector for arbitrary pasted URLs.

## Limitations

The message model was trained on general SMS data and has not been validated on a dedicated, representative dataset of gaming scams. Its output is not proof that a message is fraudulent or safe.

The server checker examines only a small number of settings. It is not a complete security audit and does not scan networks or test servers for vulnerabilities.

## Datasets and Attribution

- **SMS Spam Collection:** UCI Machine Learning Repository, https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- **Phishing Websites:** UCI Machine Learning Repository, https://archive.ics.uci.edu/dataset/327/phishing+websites

Review and include the applicable dataset licenses and attribution requirements before redistribution.

## Run Locally

1. Install Python 3 and create a virtual environment.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Ensure the trained message model exists at `models/message_model.joblib`.
4. Start the app:

   `python -m streamlit run app.py`

## Project Status

This is a hackathon prototype. Features and evaluation results should be reported according to what has actually been implemented and tested.