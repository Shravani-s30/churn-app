import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("dataset.csv")

# Drop unnecessary columns
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True, errors='ignore')

# =========================
# FEATURES & TARGET
# =========================
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Convert categorical to numeric
X = pd.get_dummies(X, drop_first=True)

#PRINT COLUMNS (IMPORTANT - copy to Streamlit)
print("MODEL COLUMNS:\n", list(X.columns))

# =========================
# TRAIN MODEL
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "model.pkl")

print("✅ Model saved successfully!")