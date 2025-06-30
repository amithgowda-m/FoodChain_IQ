import pandas as pd
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Load dataset
df = pd.read_csv("balanced_13k_dataset.csv")

# Encode product_id using LabelEncoder
le = LabelEncoder()
df["product_encoded"] = le.fit_transform(df["product_id"])

# Features and target
X = df[["product_encoded", "temperature", "humidity", "shock_level", "duration_hours"]]
y = df["spoilage_risk_level"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train LightGBM model
model = LGBMClassifier(
    objective='multiclass',
    num_class=3,
    n_estimators=200,
    learning_rate=0.05,
    max_depth=8,
    class_weight='balanced'
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("📈 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=[0, 1, 2], yticklabels=[0, 1, 2])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Save model and encoder
joblib.dump(model, "spoilage_model.txt")
joblib.dump(le, "product_encoder.pkl")
print("\n🧠 Model and encoder saved!")