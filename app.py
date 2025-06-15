import streamlit as st
import google.generativeai as genai

# Load API Key securely
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# App config
st.set_page_config(page_title="📧 Email Threat Detector", page_icon="⚠️")
st.title("📧 Email Threat Detector")
st.write("Paste the email text below and click **Analyze** to detect potential threats.")

# Input field
email_text = st.text_area("✉️ Email Body", height=300, placeholder="Paste email content here...")

# Button to trigger analysis
if st.button("🔍 Analyze"):
    if not email_text.strip():
        st.warning("Please paste the email content.")
    else:
        with st.spinner("Analyzing..."):
            prompt = f"""
You're a cybersecurity AI. Analyze the following email body and classify it as either a **threat** or **not a threat**. Provide:
1. A one-word classification: "Threat" or "Not a Threat".
2. A concise conclusive explanation of your decision.

Email Content:
\"\"\"
{email_text}
\"\"\"
"""

            response = model.generate_content(prompt)
            result = response.text.strip()

            # Basic parsing (can be improved)
            lines = result.split("\n")
            classification = lines[0].strip()
            explanation = "\n".join(lines[1:]).strip()

            # Display result
            st.subheader("🛡️ Classification")
            st.success(classification)

            st.subheader("🧠 Explanation")
            st.write(explanation)
