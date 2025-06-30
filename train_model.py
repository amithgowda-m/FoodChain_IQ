import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, 
                             confusion_matrix, 
                             accuracy_score, 
                             precision_score, 
                             recall_score, 
                             f1_score)

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv('foodchain_iq_dataset_5k.csv')

# -----------------------------
# 2. Encode Categorical Data
# -----------------------------
le = LabelEncoder()
df['Product Type Encoded'] = le.fit_transform(df['Product Type'])

# Define features and target
X = df[['Product Type Encoded', 'Temperature (°C)', 'Humidity (%)', 'Shock Level (g)']]
y = df['Risk Level']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# 3. Train Model
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# Predict
y_pred = model.predict(X_test_scaled)

# -----------------------------
# 4. Model Evaluation Metrics
# -----------------------------
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("🔍 Precision (macro):", precision_score(y_test, y_pred, average='macro'))
print("🧾 Recall (macro):", recall_score(y_test, y_pred, average='macro'))
print("📊 F1 Score (macro):", f1_score(y_test, y_pred, average='macro'))

# Classification Report
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
plt.show()

# -----------------------------
# 5. Feature Importance Visualization
# -----------------------------
feature_importances = model.feature_importances_
features = ['Product Type', 'Temperature', 'Humidity', 'Shock']
sns.barplot(x=feature_importances, y=features)
plt.title('Feature Importances')
plt.show()