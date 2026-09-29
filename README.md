# MindEase | Student Mental Health Analysis & Depression Risk Predictor

An end-to-end machine learning system and full-stack web application designed to assess student depression risk, explain key contributing factors using SHAP (Explainable AI), and deliver personalized mental health recommendations.

---

## Tech Stack

* **Machine Learning & Data Science:** Python 3, `scikit-learn`, `xgboost`, `shap`, `pandas`, `numpy`, `joblib`
* **Data Visualization:** `matplotlib`, `seaborn`
* **Backend API:** FastAPI, Uvicorn, Pydantic, PyJWT, `bcrypt`, Motor / PyMongo (with local JSON storage fallback), `python-dotenv`
* **Frontend Web App:** React 19, Vite 8, React Router 7, TailwindCSS 4, Lucide React, Axios

---

## Dataset

* **File:** [`data_clean/student_data_clean.csv`](file:///c:/Users/hp/Desktop/Projects/Student-Mental-health-analysis/data_clean/student_data_clean.csv)
* **Size:** 27,901 student records
* **Target Variable:** `Depression` (Binary: `1` = Depressed, `0` = Not Depressed; ~58.55% positive prevalence)
* **Features:** Age, Gender, CGPA, Daily Work/Study Hours, Sleep Duration, Dietary Habits, Suicidal Thoughts, Family History of Mental Illness, and Degree.

---

## Pipeline & Approach

1. **Preprocessing ([preprocess.py](file:///c:/Users/hp/Desktop/Projects/Student-Mental-health-analysis/backend/app/utils/preprocess.py)):** Excludes non-predictive columns (`id`, `Job.Satisfaction`), maps binary flags (Gender, Family History, Suicidal Thoughts), ordinally encodes sleep quality (0–4) and diet (0–3), and one-hot encodes `Degree`.
2. **Data Split ([prepare_data.py](file:///c:/Users/hp/Desktop/Projects/Student-Mental-health-analysis/notebooks/prepare_data.py)):** 80/20 stratified train-test split maintaining class balance (22,320 training rows, 5,581 testing rows).
3. **Model Training & Tuning ([train_models.py](file:///c:/Users/hp/Desktop/Projects/Student-Mental-health-analysis/notebooks/train_models.py)):** Trained and cross-validated Logistic Regression, Random Forest, and XGBoost Classifier using 5-fold Stratified K-Fold and `GridSearchCV` optimizing for F1 Score.
4. **Explainability ([explain_model.py](file:///c:/Users/hp/Desktop/Projects/Student-Mental-health-analysis/notebooks/explain_model.py)):** Utilizes SHAP `TreeExplainer` to calculate global feature importance and individual prediction attributions.
5. **Web Deployment:** Exposes prediction, SHAP attribution, user auth, and recommendation services via a FastAPI backend connected to a React single-page app.

---

## Model Results

* **Champion Model:** **XGBoost Classifier** ([`best_model.joblib`](file:///c:/Users/hp/Desktop/Projects/Student-Mental-health-analysis/backend/models/best_model.joblib))
* **Test Set Performance (5,581 samples):**
  * **Accuracy:** **84.66%** (`0.8466`)
  * **F1 Score:** **87.11%** (`0.8711`)
  * **Precision:** **85.74%** (`0.8574`)
  * **Recall:** **88.53%** (`0.8853`)
* **Key Risk Insights:** Suicidal thoughts, high academic work/study hours, and financial stress are the strongest depression risk drivers, while adequate sleep (7–8+ hours) and higher CGPA serve as key protective factors.

---

## How to Run

### 1. Backend Setup & API Server
```powershell
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server (runs on http://127.0.0.1:8000)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup
```powershell
# Navigate to frontend directory
cd frontend

# Install node dependencies
npm install

# Start Vite development server
npm run dev
```

### 3. Training & Analysis Pipeline (Optional)
To re-run data preparation, model training, or SHAP analysis:
```powershell
.\backend\venv\Scripts\python.exe notebooks/prepare_data.py
.\backend\venv\Scripts\python.exe notebooks/train_models.py
.\backend\venv\Scripts\python.exe notebooks/explain_model.py
```

---

## Project Structure

```
Student-Mental-health-analysis/
├── backend/                # FastAPI application & ML inference backend
│   ├── app/
│   │   ├── models/         # Pydantic schemas
│   │   ├── routes/         # API endpoints (auth, predict, explain, recommend)
│   │   ├── services/       # Personalized recommendation logic
│   │   ├── utils/          # Preprocessing and feature engineering helpers
│   │   ├── database.py     # MongoDB integration with JSON fallback
│   │   └── main.py         # FastAPI app initialization and CORS middleware
│   ├── models/             # Serialized champion model (best_model.joblib) & features JSON
│   └── requirements.txt    # Python dependency manifest
├── data_clean/             # Cleaned dataset (27,901 records) & train/test CSV splits
├── frontend/               # React 19 + Vite + TailwindCSS dashboard web app
└── notebooks/              # Analysis & pipeline scripts
    ├── prepare_data.py     # Data encoding and 80/20 train/test split script
    ├── eda.py              # Visualizations generator script
    ├── train_models.py     # Grid search model evaluation script
    └── explain_model.py   # SHAP explainability script
```
