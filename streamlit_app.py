import streamlit as st
import requests
import time


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Spam Email Detector",
    page_icon="📧",
    layout="wide"
)


# ---------------- API CONFIG ----------------
API_URL = "http://127.0.0.1:8000/predict"


# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>

    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
    }

    .title {
        font-size: 52px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 20px;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 40px;
    }

    .card {
        background-color: #1e293b;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    .result-spam {
        color: #ef4444;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }

    .result-ham {
        color: #22c55e;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 50px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">📧 AI Spam Email Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Spam Detection System</div>',
    unsafe_allow_html=True
)


# ---------------- LAYOUT ----------------
left_col, right_col = st.columns([2, 1])


# ---------------- LEFT PANEL ----------------
with left_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("✉️ Enter Email Content")

    email_text = st.text_area(
        "",
        height=400,
        placeholder="Paste email text here..."
    )

    predict_button = st.button(
        "🚀 Predict Spam",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- RIGHT PANEL ----------------
with right_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Prediction Result")

    if predict_button:

        if email_text.strip() == "":
            st.warning("Please enter email text.")

        else:

            try:

                with st.spinner("Analyzing email..."):

                    start_time = time.time()

                    response = requests.post(
                        API_URL,
                        json={"email": email_text},
                        timeout=5
                    )

                    end_time = time.time()

                    latency = end_time - start_time

                if response.status_code == 200:

                    result = response.json()

                    prediction = result["prediction"]
                    confidence = result["confidence"]

                    if prediction == "spam":

                        st.markdown(
                            '<div class="result-spam">🚨 SPAM DETECTED</div>',
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            '<div class="result-ham">✅ SAFE EMAIL</div>',
                            unsafe_allow_html=True
                        )

                    st.metric(
                        "Confidence Score",
                        f"{confidence * 100:.2f}%"
                    )

                    st.progress(float(confidence))

                    st.metric(
                        "API Latency",
                        f"{latency:.3f} sec"
                    )

                else:
                    st.error(f"API Error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("FastAPI server is not running.")

            except requests.exceptions.Timeout:
                st.error("Request timed out.")

            except Exception as e:
                st.error(f"Unexpected Error: {e}")

    else:
        st.info("Prediction result will appear here.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class="footer">
        Built with FastAPI + Streamlit + Scikit-learn
    </div>
    """,
    unsafe_allow_html=True
)