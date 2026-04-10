import streamlit as st
import mysql.connector
import traceback


# =========================
# DATABASE CONNECTION
# =========================
def connect_db():
    return mysql.connector.connect(
        host=st.secrets["MYSQLHOST"],
        user=st.secrets["MYSQLUSER"],
        password=st.secrets["MYSQLPASSWORD"],
        database=st.secrets["MYSQLDATABASE"],
        port=int(st.secrets["MYSQLPORT"])
    )


# =========================
# SAVE PREDICTION FUNCTION
# =========================
def save_prediction(data, pred):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO predictions 
        (
            CreditScore,
            Age,
            Tenure,
            Balance,
            NumOfProducts,
            HasCrCard,
            IsActiveMember,
            EstimatedSalary,
            prediction
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data["CreditScore"],
            data["Age"],
            data["Tenure"],
            data["Balance"],
            data["NumOfProducts"],
            data["HasCrCard"],
            data["IsActiveMember"],
            data["EstimatedSalary"],
            pred
        )

        print("🔵 INSERT VALUES:", values)

        cursor.execute(query, values)
        conn.commit()

        print("✅ Data inserted successfully into Railway DB")

    except Exception as e:
        print("❌ DATABASE ERROR OCCURRED")
        traceback.print_exc()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()