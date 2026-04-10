import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib

# Load data
df = pd.read_csv("dataset.csv")

# Drop useless columns
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True, errors='ignore')

# Split features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Convert categorical to numeric
X = pd.get_dummies(X, drop_first=True)

# ✅ SAVE COLUMNS HERE (IMPORTANT)
joblib.dump(X.columns, "columns.pkl")

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")

print("Model and columns saved successfully!")