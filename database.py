
import streamlit as st
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host=st.secrets["MYSQLHOST"],
        user=st.secrets["MYSQLUSER"],
        password=st.secrets["MYSQLPASSWORD"],
        database=st.secrets["MYSQLDATABASE"],
        port=int(st.secrets["MYSQLPORT"])
    )



def save_prediction(data, pred):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO predictions 
        (CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, prediction)
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
            pred   # ✅ CHURN / STAY
        )

        cursor.execute(query, values)
        conn.commit()

        print("✅ Data inserted successfully")

    except Exception as e:
        import traceback
        print("❌ Database Error:")
        traceback.print_exc()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()