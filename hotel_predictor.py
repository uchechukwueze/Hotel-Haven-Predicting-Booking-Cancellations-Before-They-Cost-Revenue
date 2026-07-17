import streamlit as st
import joblib
import numpy as np
import pandas as pd
import base64
from pathlib import Path


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="Hotel Haven Booking Cancellation Predictor",
    page_icon="🏨",
    layout="wide"
)


# ==============================
# CUSTOM CSS
# ==============================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #07111f, #0f172a);
    }

    .hero-box {
        background: linear-gradient(135deg, #0f4c81, #2563eb);
        padding: 42px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 8px 28px rgba(0,0,0,0.35);
    }

    .hero-box h1 {
        font-size: 46px;
        margin-bottom: 10px;
        font-weight: 900;
    }

    .hero-box p {
        font-size: 18px;
        color: #eaf2ff;
        margin: 0;
    }

    .section-card {
        background: #111827;
        color: white !important;
        padding: 26px;
        border-radius: 20px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.30);
        margin-bottom: 22px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .section-card h3 {
        color: #93c5fd !important;
        margin-bottom: 12px;
        font-weight: 800;
    }

    .section-card p {
        color: #f3f4f6 !important;
        font-size: 15px;
        line-height: 1.6;
    }

    .section-card b {
        color: white !important;
    }

    .small-text {
        color: #d1d5db !important;
        font-size: 14px;
    }

    .stSlider label, .stNumberInput label, .stSelectbox label {
        color: white !important;
        font-weight: 600;
    }

    .stFormSubmitButton>button {
        background: linear-gradient(135deg, #2563eb, #0f4c81);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 28px;
        font-size: 18px;
        font-weight: 800;
        width: 100%;
        transition: 0.3s ease;
    }

    .stFormSubmitButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8, #08365f);
        color: white;
        transform: scale(1.02);
    }

    .cancel-card {
        background: linear-gradient(135deg, #450a0a, #991b1b);
        padding: 34px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.35);
        border-left: 8px solid #ef4444;
        margin-top: 25px;
    }

    .safe-card {
        background: linear-gradient(135deg, #052e16, #047857);
        padding: 34px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.35);
        border-left: 8px solid #22c55e;
        margin-top: 25px;
    }

    .result-title {
        color: white;
        font-size: 38px;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .result-subtitle {
        color: #f3f4f6;
        font-size: 17px;
        line-height: 1.6;
    }

    .probability-box {
        background: #111827;
        padding: 22px;
        border-radius: 18px;
        margin-top: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0px 6px 20px rgba(0,0,0,0.30);
    }

    .footer-card {
        background: #111827;
        padding: 28px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.30);
        margin-top: 45px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .footer-card img {
        width: 95px;
        height: 95px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #60a5fa;
        margin-bottom: 12px;
    }

    .footer-title {
        color: #93c5fd;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .footer-subtitle {
        color: #f3f4f6;
        font-size: 15px;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# HELPER FUNCTION FOR IMAGE
# ==============================

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# ==============================
# LOAD MODEL
# ==============================

@st.cache_resource
def load_model():
    model = joblib.load("gb_booking_model.pkl")
    return model


model = load_model()


# ==============================
# APP HEADER
# ==============================

st.markdown(
    """
    <div class="hero-box">
        <h1>🏨 Hotel Haven Booking Cancellation Predictor</h1>
        <p>
            Predict whether a hotel booking is likely to be cancelled using booking and guest information.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==============================
# MAIN LAYOUT
# ==============================

left_col, right_col = st.columns([2, 1])


# ==============================
# LEFT SIDE: INPUT FORM
# ==============================

with left_col:
    st.markdown(
        """
        <div class="section-card">
            <h3>📝 Enter Booking Details</h3>
            <p class="small-text">
                Fill in the booking information below and click the prediction button.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("booking_prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            lead_time = st.slider(
                "📅 Lead Time",
                min_value=0,
                max_value=500,
                value=50
            )

            avg_price = st.number_input(
                "💰 Average Price Per Room",
                min_value=0,
                max_value=500,
                value=100
            )

            special_requests = st.slider(
                "⭐ Number of Special Requests",
                min_value=0,
                max_value=5,
                value=1
            )

        with col2:
            total_guests = st.slider(
                "👥 Total Guests",
                min_value=1,
                max_value=10,
                value=2
            )

            total_nights = st.slider(
                "🌙 Total Nights",
                min_value=1,
                max_value=20,
                value=3
            )

            repeated_guest = st.selectbox(
                "🔁 Repeated Guest?",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No"
            )

        submitted = st.form_submit_button("🔮 Predict Cancellation")


# ==============================
# RIGHT SIDE: PROJECT INFORMATION
# ==============================

with right_col:
    st.markdown(
        """
        <div class="section-card">
            <h3>📊 Model Information</h3>
            <p><b>Model:</b> Random Forest Model</p>
            <p><b>Task:</b> Booking Cancellation Classification</p>
            <p><b>Output:</b> Canceled or Not Canceled</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>💡 Business Meaning</h3>
            <p>
                This app helps hotels estimate whether a booking may be cancelled,
                so they can plan room allocation and revenue management more effectively.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>🎯 Why It Matters</h3>
            <p>
                Booking cancellations can affect hotel revenue, staffing, and occupancy planning.
                Early prediction helps hotels make better operational decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================
# PREDICTION LOGIC
# ==============================

if submitted:
    input_data = np.array([[
        lead_time,
        avg_price,
        special_requests,
        total_guests,
        total_nights,
        repeated_guest
    ]])

    prediction = model.predict(input_data)[0]

    proba = model.predict_proba(input_data)[0]

    not_canceled_prob = proba[0]
    canceled_prob = proba[1]

    st.markdown("---")

    if prediction == 1:
        st.markdown(
            f"""
            <div class="cancel-card">
                <div class="result-title">⚠️ Booking Likely to Be Canceled</div>
                <div class="result-subtitle">
                    The model predicts that this booking may be cancelled.
                    Cancellation probability: <b>{canceled_prob:.2%}</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.balloons()

        st.markdown(
            f"""
            <div class="safe-card">
                <div class="result-title">✅ Booking Not Likely to Be Canceled</div>
                <div class="result-subtitle">
                    The model predicts that this booking is likely to remain active.
                    Not-canceled probability: <b>{not_canceled_prob:.2%}</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="probability-box">
            <h3 style="color:#93c5fd;">📈 Prediction Probability</h3>
            <p style="color:white;"><b>Not Canceled:</b> {not_canceled_prob:.2%}</p>
            <p style="color:white;"><b>Canceled:</b> {canceled_prob:.2%}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🔍 View model input used for prediction"):
        input_df = pd.DataFrame({
            "Lead Time": [lead_time],
            "Average Price Per Room": [avg_price],
            "Special Requests": [special_requests],
            "Total Guests": [total_guests],
            "Total Nights": [total_nights],
            "Repeated Guest": [repeated_guest]
        })

        st.dataframe(input_df, use_container_width=True)

else:
    st.info("Please enter the booking details and click **Predict Cancellation**.")


# ==============================
# FOOTER WITH YOUR PICTURE
# ==============================

BASE_DIR = Path(__file__).parent
profile_image_path = BASE_DIR / "uchechukwu.jpg"

st.markdown("<br>", unsafe_allow_html=True)

if profile_image_path.exists():
    profile_img = image_to_base64(profile_image_path)

    st.markdown(
        f"""
        <div class="footer-card">
            <img src="data:image/jpeg;base64,{profile_img}">
            <p class="footer-title">
                Built with Streamlit and Machine Learning
            </p>
            <p class="footer-subtitle">
                Hotel Booking Cancellation Prediction Project | Uchechukwu Eze
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.markdown(
        """
        <div class="footer-card">
            <p class="footer-title">
                Built with Streamlit and Machine Learning
            </p>
            <p class="footer-subtitle">
                Hotel Booking Cancellation Prediction Project | Uchechukwu Eze
            </p>
            <p style="color:#9ca3af; font-size:13px; margin-top:8px;">
                Add your profile image as <b>uchechukwu.jpg</b> in the same folder as app.py.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )