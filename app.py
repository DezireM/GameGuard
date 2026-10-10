
from pathlib import Path
import sys

import joblib
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from server_auditor import audit_server_properties

st.set_page_config(
    page_title="GameGuard",
    page_icon="🛡️",
    layout="centered",
)

MODEL_PATH = ROOT / "models" / "message_model.joblib"


def explain_message_risks(message):
    """Identify possible warning signs using transparent text rules."""
    text = message.lower()
    warnings = []

    patterns = [
        (
            ["password", "verification code", "2fa code", "login details"],
            "The message mentions passwords, verification codes, or login details.",
        ),
        (
            ["click here", "verify now", "claim now", "http://", "https://"],
            "The message includes a link or asks you to take an immediate action.",
        ),
        (
            [
                "urgent",
                "immediately",
                "within 24 hours",
                "account will be banned",
                "account suspended",
                "expires soon",
            ],
            "The message uses urgency or threatens an account-related consequence.",
        ),
        (
            [
                "free skins",
                "free robux",
                "free v-bucks",
                "free rewards",
                "unlimited coins",
                "you won",
            ],
            "The message advertises free rewards or a prize.",
        ),
        (
            ["send me", "give me your", "share your"],
            "The message asks you to provide or share information.",
        ),
    ]

    for keywords, explanation in patterns:
        if any(keyword in text for keyword in keywords):
            warnings.append(explanation)

    if not warnings:
        warnings.append(
            "No warning signs covered by GameGuard's simple text rules "
            "were found. Other risks may still be present."
        )

    return warnings

def recommend_safe_actions(message):
    """Suggest practical actions based on detected warning signs."""
    text = message.lower()
    actions = []

    if any(word in text for word in [
        "password", "verification code", "2fa code", "login details"
    ]):
        actions.append(
            "Account protection: Do not share passwords or verification "
            "codes. If you already shared them, change your password "
            "through the official service and secure your account."
        )

    if any(word in text for word in [
        "http://", "https://", "click here", "verify now", "claim now"
    ]):
        actions.append(
            "Link safety: Do not open unexpected links. Visit the game's "
            "official website by typing its address yourself."
        )

    if any(word in text for word in [
        "free skins", "free robux", "free v-bucks", "free rewards",
        "unlimited coins", "you won"
    ]):
        actions.append(
            "Reward verification: Check whether the offer appears on an "
            "official game channel. Never provide account credentials "
            "to claim a reward."
        )

    if any(word in text for word in [
        "urgent", "immediately", "within 24 hours",
        "account will be banned", "account suspended", "expires soon"
    ]):
        actions.append(
            "Pressure tactics: Pause before acting. Check account "
            "warnings directly through the game's official launcher "
            "or website."
        )

    if not actions:
        actions.append(
            "General precaution: Verify the sender independently, "
            "avoid sharing sensitive information, and be cautious "
            "with unexpected requests."
        )

    return actions



st.title("🛡️ GameGuard")
st.subheader("Gaming scam awareness and server security")

st.write(
    "Check suspicious gaming messages and review selected Minecraft "
    "Java server settings for potential security risks."
)

st.warning(
    "Prototype: the message model was trained on general SMS spam data, "
    "not a dedicated gaming-scam dataset. Server checks cover only a few "
    "settings. Neither feature can prove something is safe."
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


if not MODEL_PATH.exists():
    st.error("Message model not found. Train it before running GameGuard.")
    st.stop()

model = load_model()

message_tab, server_tab = st.tabs(
    ["🎮 Message Checker", "🛡️ Minecraft Server Check"]
)

with message_tab:
    st.header("Check a suspicious message")

    message = st.text_area(
        "Paste a gaming message",
        placeholder="Example: Claim your free skins now...",
        height=150,
        key="gaming_message",
    )

    if st.button("Analyze message", type="primary", key="analyze_message"):
        if not message.strip():
            st.warning("Please enter a message first.")
        else:
            prediction = model.predict([message])[0]
            probabilities = model.predict_proba([message])[0]
            classes = list(model.classes_)
            spam_probability = float(
                probabilities[classes.index("spam")]
            )

            st.subheader("Analysis result")
            st.metric("Spam probability", f"{spam_probability:.1%}")

            if prediction == "spam":
                st.error("Spam-like language detected")
            else:
                st.info("The model did not classify this as spam.")

        
            
            warnings = explain_message_risks(message)

            st.subheader("Security assessment")

            if len(warnings) >= 2 and not warnings[0].startswith(
                "No warning signs"
            ):
                st.warning(
                    f"Multiple warning signs found ({len(warnings)}). "
                    "Review the evidence before interacting with this message."
                )
            elif warnings[0].startswith("No warning signs"):
                st.info(
                    "No warning signs covered by the current rules were found. "
                    "This does not guarantee that the message is safe."
                )
            else:
                st.warning(
                    "A potential warning sign was found. "
                    "Check the evidence below."
                )

            st.subheader("Evidence")

            for warning in warnings:
                st.write(f"• {warning}")


            
            st.caption(
                "This is the model's estimated class probability, "
                "not a calibrated real-world scam probability."
            )

            st.subheader("Recommended next steps")

            for action in recommend_safe_actions(message):
                st.write(f"🛡️ {action}")

            st.caption(
                "These recommendations use simple keyword rules and are not "
                "proof that a message is fraudulent."
            )


with server_tab:
    st.header("Review Minecraft server settings")

    st.write(
        "Paste selected lines from your Minecraft Java Edition "
        "server.properties file. GameGuard checks only the settings "
        "listed in its current prototype."
    )

    config_text = st.text_area(
        "Server configuration",
        value=(
            "online-mode=true\n"
            "white-list=true\n"
            "enable-rcon=false\n"
        ),
        height=180,
        key="server_config",
    )

    if st.button("Check server settings", type="primary"):
        findings = audit_server_properties(config_text)

        st.subheader("Audit findings")

        for finding in findings:
            severity = finding["severity"]
            heading = f"{severity}: {finding['setting']}"

            if severity == "HIGH":
                st.error(heading)
            elif severity == "MEDIUM":
                st.warning(heading)
            else:
                st.info(heading)

            st.write(finding["finding"])
            st.write(f"**Recommendation:** {finding['recommendation']}")

        st.caption(
            "This is a limited configuration review, not a complete "
            "security audit or a guarantee that your server is secure."
        )

st.divider()
st.caption("GameGuard • ForgeHacks prototype")
