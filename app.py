import streamlit as st
import joblib
import pandas as pd
from database import save_prediction

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Churn Predictor",
    page_icon="💖",
    layout="centered"
)

# =========================
# UI STYLE (ANIMATED)
# =========================
st.markdown("""
<style>

/* Background Animation */
.stApp {
    background: linear-gradient(-45deg, #a1c4fd, #c2e9fb, #fbc2eb, #fad0c4);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Main container */
.block-container {
    background: rgba(255,255,255,0.9);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* Section Cards */
.card {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    background: rgba(255,255,255,0.8);
    border: 1px solid #e5e7eb;
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from {opacity:0; transform: translateY(10px);}
    to {opacity:1; transform: translateY(0);}
}

/* Title */
h1 {
    text-align: center;
    color: #4c1d95;
    font-weight: 800;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #ff9a9e, #fad0c4);
    color: #4c1d95;
    font-size: 18px;
    font-weight: 700;
    padding: 0.8rem;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* Result */
.result-box {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-weight: 700;
    margin-top: 20px;
    animation: pop 0.5s ease;
}

@keyframes pop {
    from {transform: scale(0.8); opacity: 0;}
    to {transform: scale(1); opacity: 1;}
}

.success {background: #d1fae5; color: #065f46;}
.error {background: #fee2e2; color: #7f1d1d;}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

# =========================
# HEADER
# =========================
st.title("Customer Churn Predictor")
# st.caption("✨ Smart + Cute AI Prediction")

# =========================
# FORM (NEW STRUCTURE)
# =========================
with st.form("churn_form"):

    # -------- Section 1 --------
    st.subheader("👤 Customer Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        credit = st.number_input("Credit Score", min_value=0)
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        geo = st.selectbox("Geography", ["France", "Germany", "Spain"])
        tenure = st.number_input("Tenure", min_value=0)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Section 2 --------
    
    st.subheader("💳 Account Details")

    col3, col4 = st.columns(2)
    with col3:
        balance = st.number_input("Balance", min_value=0.0)
        products = st.number_input("Products", min_value=1)
    with col4:
        card = st.selectbox("Credit Card", [0, 1])
        active = st.selectbox("Active Member", [0, 1])

    salary = st.number_input("Estimated Salary", min_value=0.0)

    st.markdown('</div>', unsafe_allow_html=True)

    # Submit Button
    submitted = st.form_submit_button("🚀 Predict Now")

# =========================
# PREDICTION
# =========================
if submitted:

    data = pd.DataFrame([{
        "CreditScore": credit,
        "Geography": geo,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": products,
        "HasCrCard": card,
        "IsActiveMember": active,
        "EstimatedSalary": salary
    }])

    data = pd.get_dummies(data)
    data = data.reindex(columns=columns, fill_value=0)

    pred = model.predict(data)[0]
    label = "CHURN" if pred == 1 else "STAY"

    if label == "CHURN":
        st.markdown('<div class="result-box error">⚠️ Customer may CHURN 💔</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box success">🎉 Customer will STAY 💖</div>', unsafe_allow_html=True)

    # Save
    save_prediction({
        "CreditScore": credit,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": products,
        "HasCrCard": card,
        "IsActiveMember": active,
        "EstimatedSalary": salary
    }, label)

    st.success("✔ Saved successfully")