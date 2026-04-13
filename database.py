import streamlit as st
import mysql.connector
import traceback

def connect_db():
    return mysql.connector.connect(
        host=st.secrets["MYSQLHOST"],
        user=st.secrets["MYSQLUSER"],
        password=st.secrets["MYSQLPASSWORD"],
        database=st.secrets["MYSQLDATABASE"],
        port=int(st.secrets["MYSQLPORT"]),
        connection_timeout=30,
        auth_plugin='mysql_native_password'
    )

def save_prediction(data, pred):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO predictions 
        (
            CreditScore, Age, Tenure, Balance,
            NumOfProducts, HasCrCard, IsActiveMember,
            EstimatedSalary, prediction
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

        cursor.execute(query, values)
        conn.commit()

    except Exception:
        print("❌ DATABASE ERROR")
        traceback.print_exc()

    finally:
        # 🔥 SAFE CLOSE
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()