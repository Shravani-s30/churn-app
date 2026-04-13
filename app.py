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
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# 🔥 HARDCODED COLUMNS (COPY FROM TRAIN OUTPUT)
MODEL_COLUMNS = [
    'CreditScore','Age','Tenure','Balance','NumOfProducts',
    'HasCrCard','IsActiveMember','EstimatedSalary',
    'Geography_Germany','Geography_Spain','Gender_Male'
]

# =========================
# UI
# =========================
st.title("💖 Customer Churn Predictor")

with st.form("churn_form"):

    st.subheader("👤 Customer Profile")

    col1, col2 = st.columns(2)
    with col1:
        credit = st.number_input("Credit Score", min_value=0)
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        geo = st.selectbox("Geography", ["France", "Germany", "Spain"])
        tenure = st.number_input("Tenure", min_value=0)

    st.subheader("💳 Account Details")

    col3, col4 = st.columns(2)
    with col3:
        balance = st.number_input("Balance", min_value=0.0)
        products = st.number_input("Products", min_value=1)
    with col4:
        card = st.selectbox("Credit Card", [0, 1])
        active = st.selectbox("Active Member", [0, 1])

    salary = st.number_input("Estimated Salary", min_value=0.0)

    submitted = st.form_submit_button("🚀 Predict Now")

# =========================
# PREDICTION
# =========================
if submitted:

    # 🔥 Create full feature structure
    input_dict = {
        'CreditScore': credit,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': products,
        'HasCrCard': card,
        'IsActiveMember': active,
        'EstimatedSalary': salary,
        'Geography_Germany': 0,
        'Geography_Spain': 0,
        'Gender_Male': 0
    }

    # Encoding logic
    if geo == "Germany":
        input_dict['Geography_Germany'] = 1
    elif geo == "Spain":
        input_dict['Geography_Spain'] = 1

    if gender == "Male":
        input_dict['Gender_Male'] = 1

    # Convert to DataFrame
    data = pd.DataFrame([input_dict])

    # Ensure correct column order
    data = data[MODEL_COLUMNS]

    # Prediction
    pred = model.predict(data)[0]
    label = "CHURN" if pred == 1 else "STAY"

    # Output
    if label == "CHURN":
        st.error("⚠️ Customer may CHURN 💔")
    else:
        st.success("🎉 Customer will STAY 💖")

    # Save to DB
    save_prediction(input_dict, label)

    st.success("✔ Saved successfully")