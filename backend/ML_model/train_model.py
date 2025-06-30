import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                             accuracy_score, precision_score, 
                             recall_score, f1_score)

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv('foodchain_iq_dataset_5k.csv')

# Optional: If duration is available
# df['Duration (hrs)'] = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.total_seconds() / 3600

# -----------------------------
# 2. One-Hot Encode Product Type
# -----------------------------
df_encoded = pd.get_dummies(df[['Product Type']], prefix='Product', drop_first=True)

# -----------------------------
# 3. Combine Features
# -----------------------------
X = pd.concat([
    df_encoded,
    df[['Temperature (°C)', 'Humidity (%)', 'Shock Level (g)']]
    # , df[['Duration (hrs)']]   # Uncomment if duration exists
], axis=1)

y = df['Risk Level']

# -----------------------------
# 4. Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 5. Feature Scaling
# -----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# 6. Train Random Forest Model
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# -----------------------------
# 7. Make Predictions
# -----------------------------
y_pred = model.predict(X_test_scaled)

# -----------------------------
# 8. Evaluation Metrics
# -----------------------------
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("🔍 Precision (macro):", precision_score(y_test, y_pred, average='macro'))
print("🧾 Recall (macro):", recall_score(y_test, y_pred, average='macro'))
print("📊 F1 Score (macro):", f1_score(y_test, y_pred, average='macro'))

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Safe (0)', 'Spoiled (1)']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Predicted Safe', 'Predicted Spoiled'],
            yticklabels=['Actual Safe', 'Actual Spoiled'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.show()

# -----------------------------
# 9. Feature Importance Plot
# -----------------------------
importances = model.feature_importances_
feature_names = X.columns

plt.figure(figsize=(8, 6))
sns.barplot(x=importances, y=feature_names)
plt.title('Feature Importances')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()

# -----------------------------
# 10. Save Model & Scaler
# -----------------------------
joblib.dump(model, 'rf_spoilage_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("✅ Model and scaler saved!")
