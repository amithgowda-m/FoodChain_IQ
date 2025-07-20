# 🚚🥗 FoodChain_IQ - Smart Food Spoilage Detection System

**FoodChain_IQ** is an AI-powered food logistics quality monitoring system that detects potential spoilage during transportation using sensor data and machine learning. It helps logistics managers and businesses ensure food safety by detecting temperature abuse, humidity issues, and shock damage in real-time.

---

## 🧠 Key Features

- 🌡️ Real-time monitoring of **Temperature**, **Humidity**, and **Shock Level**
- 🔍 Machine Learning model (Random Forest) for spoilage risk prediction
- 🧾 Multi-class classification: `Safe (0)`, `At Risk (1)`, `Spoiled (2)`
- 📉 Visualizations: Confusion Matrix, Feature Importance
- ⚙️ Scalable and FastAPI-ready backend
- 📊 Model, scaler, and training column export using `joblib`

---

## 📊 Dataset Details

The dataset (`foodchain_iq_dataset_5k.csv`) contains:
- `Product Type` (e.g., Fruits, Vegetables, Dairy)
- `Temperature (°C)`
- `Humidity (%)`
- `Shock Level (g)`
- `Risk Level` (0: Safe, 1: At Risk, 2: Spoiled)

---

## 🔬 Model Training Pipeline

### 1. Load and preprocess the data
- One-hot encode `Product Type`
- Combine sensor features
- Train-test split (80:20)
- Standardization using `StandardScaler`

### 2. Train the model
- Classifier: `RandomForestClassifier` with `class_weight='balanced'`
- Evaluation: Accuracy, Precision, Recall, F1-score
- Visualization: Confusion Matrix and Feature Importance

### 3. Save model artifacts
Artifacts are saved in `backend/ML_model/artifacts/`:
- `rf_spoilage_model.pkl`
- `scaler.pkl`
- `X_train_columns.pkl`

---

## 🚀 How to Run
Here you go, my friend — your clean, beautiful **`README.md` section** for **“How to Run the Project”** (ready to paste directly):

---

## 🚀 How to Run the Project

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/your-username/FoodChain_IQ.git
cd FoodChain_IQ
```

---

### ⚙️ 2. Run the FastAPI Backend

Install required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

✅ Server running at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

* Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 💻 3. Run the Frontend (React App)

Make sure you have **Node.js** and **npm** installed.

```bash
cd ../frontend
npm install
npm start
```

✅ Frontend runs at: [http://localhost:3000](http://localhost:3000)

---

### 📡 4. ESP32 / IoT Device Integration

Your ESP32 sends real-time sensor data (`temperature`, `humidity`, `shock`, `truck_id`) to:

```
POST http://127.0.0.1:8000/predict
```

### Example Payload:

```json
{
  "temperature": 9.8,
  "humidity": 85.2,
  "shock": 1.7,
  "product_type": "Fruits"
}


