
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
                st.write(
                    "Pause before clicking links or sharing passwords, "
                    "verification codes, or payment information."
                )
            else:
                st.info("The model did not classify this as spam.")
                st.write(
                    "This does not mean the message is safe. Check "
                    "the sender and links independently."
                )

            st.caption(
                "This is the model's estimated class probability, "
                "not a calibrated real-world scam probability."
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
            heading = (
                f"{severity}: {finding['setting']}"
            )

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
