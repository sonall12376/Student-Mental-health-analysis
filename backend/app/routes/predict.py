import os
import uuid
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from app.config import settings
from app.database import get_history_collection
from app.routes.auth import get_current_user
from app.models.schemas import AssessmentInput, PredictionResponse, SHAPFactor, HistoryRecord
from app.utils.preprocess import preprocess_features
from app.services.recommendation_service import generate_personalized_recommendations
import shap

router = APIRouter(tags=["Depression Prediction"])

# Global placeholders for lazy loading model and features to optimize startup
_model = None
_features = None
_explainer = None

def get_model():
    """Lazy load the serialized XGBoost ML model."""
    global _model
    if _model is None:
        if not os.path.exists(settings.MODEL_PATH):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Serialized model file not found at {settings.MODEL_PATH}. Make sure Phase 4 completed."
            )
        _model = joblib.load(settings.MODEL_PATH)
    return _model

def get_features():
    """Lazy load the expected preprocessed feature columns list."""
    global _features
    if _features is None:
        if not os.path.exists(settings.FEATURES_PATH):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Features list JSON file not found at {settings.FEATURES_PATH}."
            )
        with open(settings.FEATURES_PATH, "r") as f:
            _features = json.load(f)
    return _features

def get_explainer():
    """Lazy load the SHAP TreeExplainer."""
    global _explainer
    if _explainer is None:
        model = get_model()
        # Initialize SHAP explainer on our model
        _explainer = shap.TreeExplainer(model)
    return _explainer

# Map Pydantic snake_case input fields to the dot-notation CSV columns expected by preprocessor
KEY_MAPPING = {
    "gender": "Gender",
    "age": "Age",
    "academic_pressure": "Academic.Pressure",
    "cgpa": "CGPA",
    "study_satisfaction": "Study.Satisfaction",
    "sleep_duration": "Sleep.Duration",
    "dietary_habits": "Dietary.Habits",
    "degree": "Degree",
    "have_you_ever_had_suicidal_thoughts": "Have.you.ever.had.suicidal.thoughts..",
    "work_study_hours": "Work.Study.Hours",
    "financial_stress": "Financial.Stress",
    "family_history_of_mental_illness": "Family.History.of.Mental.Illness"
}

# Student-friendly explanation templates for features based on whether SHAP is positive (risk) or negative (protective)
FEATURE_EXPLANATIONS = {
    "Academic.Pressure": {
        "positive": "High academic workload is significantly pushing up your stress levels.",
        "negative": "Your manageable academic workload is acting as a helpful protective factor."
    },
    "Financial.Stress": {
        "positive": "Anxiety surrounding finances is heavily contributing to your mental load.",
        "negative": "Low financial stress is supporting your mental stability."
    },
    "Sleep.Duration": {
        "positive": "Lack of adequate sleep or irregular rest is severely dropping your energy and mood.",
        "negative": "Getting healthy, regular sleep is significantly protecting your mental well-being."
    },
    "Dietary.Habits": {
        "positive": "Unhealthy or irregular eating habits are negatively impacting your overall mood.",
        "negative": "Maintaining structured, nutritious meals is supporting your gut-brain resilience."
    },
    "Study.Satisfaction": {
        "positive": "Feeling disconnected or unsatisfied with your studies is draining your motivation.",
        "negative": "High satisfaction with your academic major is a major protective buffer."
    },
    "Work.Study.Hours": {
        "positive": "Spending excessive daily hours on study/work is creating burnout risk.",
        "negative": "Keeping balanced daily work/study hours is helping you maintain a healthy lifestyle."
    },
    "Have.you.ever.had.suicidal.thoughts..": {
        "positive": "Experiencing suicidal thoughts is a critical indicator of severe mental distress.",
        "negative": "Absence of suicidal thoughts is a positive health indicator."
    },
    "Family.History.of.Mental.Illness": {
        "positive": "A family history of mental illness slightly increases baseline genetic vulnerability.",
        "negative": "No family history of mental illness reduces background risk factors."
    },
    "Age": {
        "positive": "Your current age cohort is associated with specific life stage stressors.",
        "negative": "Age-related experience is helping buffer stressors."
    },
    "Gender": {
        "positive": "Sociological or biological gender dynamics are slightly adding to mental load.",
        "negative": "Gender-related environmental factors are in a balanced state."
    },
    "CGPA": {
        "positive": "A lower CGPA is adding to academic worry and self-esteem strain.",
        "negative": "Your strong academic standing (CGPA) is a major protective buffer."
    }
}

def get_feature_description(feature_name: str, shap_val: float) -> str:
    """Get student-friendly explanations based on the feature and its SHAP contribution direction."""
    # Handle one-hot encoded degree columns separately
    if feature_name.startswith("Degree_"):
        degree_name = feature_name.split("_")[1]
        if shap_val > 0:
            return f"Course demands in the {degree_name} program are adding to your stress."
        else:
            return f"Being in the {degree_name} major is positive or neutral for your risk profile."
            
    # Lookup feature templates
    templates = FEATURE_EXPLANATIONS.get(feature_name)
    if templates:
        return templates["positive"] if shap_val > 0 else templates["negative"]
    
    return f"{feature_name} has a {'positive' if shap_val > 0 else 'negative'} influence on your profile."

def determine_risk_level(prob: float) -> str:
    """Map probability percentage to a categorical risk score."""
    if prob < 0.35:
        return "Low"
    elif prob < 0.70:
        return "Moderate"
    else:
        return "High"


# ==========================================
# Endpoints
# ==========================================

@router.post("/predict", response_model=PredictionResponse)
def predict_depression_risk(assessment: AssessmentInput, current_user: dict = Depends(get_current_user)):
    """
    Predict depression risk, calculate SHAP explanations, generate recommendations,
    and save the record in MongoDB.
    """
    model = get_model()
    features = get_features()
    explainer = get_explainer()
    
    # 1. Translate Pydantic input keys to original dot-separated dataset column names
    raw_dict = {}
    assessment_dict = assessment.model_dump()
    for snake_k, raw_k in KEY_MAPPING.items():
        raw_dict[raw_k] = assessment_dict[snake_k]
        
    # 2. Convert to single-row Pandas DataFrame
    raw_df = pd.DataFrame([raw_dict])
    
    # 3. Preprocess DataFrame (maps ordinal, binary, and expands degree to 28 one-hot dummies)
    preprocessed_df = preprocess_features(raw_df, trained_columns=features)
    
    # 4. Model Prediction
    # predict_proba returns [prob_class_0, prob_class_1]
    probabilities = model.predict_proba(preprocessed_df)[0]
    prob_depression = float(probabilities[1])
    prediction = int(model.predict(preprocessed_df)[0])
    
    # 5. Risk Category Mapping
    risk_level = determine_risk_level(prob_depression)
    
    # 6. Dynamic SHAP Explanations
    # Compute Shapley values for this single instance
    shap_output = explainer(preprocessed_df)
    shap_vals = shap_output[0].values
    
    # Format SHAP attributions
    top_factors = []
    for feat_name, sv, fv in zip(features, shap_vals, shap_output[0].data):
        # We only care about active features or continuous variables.
        # Skip degree one-hot features that are inactive (value == 0) to avoid cluttering the report
        if feat_name.startswith("Degree_") and fv == 0:
            continue
            
        desc = get_feature_description(feat_name, sv)
        top_factors.append(SHAPFactor(
            feature=feat_name,
            feature_value=float(fv),
            shap_value=float(sv),
            description=desc
        ))
        
    # Sort factors by absolute impact size (absolute SHAP value)
    top_factors.sort(key=lambda x: abs(x.shap_value), reverse=True)
    
    # Limit to top 5 most impactful drivers
    top_5_factors = top_factors[:5]
    
    # 7. Generate Personalized Recommendations
    recommendations = generate_personalized_recommendations(assessment, risk_level)
    
    # 8. Save Record to MongoDB History
    history_col = get_history_collection()
    assessment_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    record = {
        "assessment_id": assessment_id,
        "username": current_user["username"],
        "input_data": assessment_dict,
        "depression_probability": prob_depression,
        "depression_prediction": prediction,
        "risk_level": risk_level,
        # Save top factors and recommendations as sub-documents
        "top_factors": [tf.model_dump() for tf in top_5_factors],
        "recommendations": recommendations,
        "timestamp": timestamp
    }
    history_col.insert_one(record)
    
    return {
        "assessment_id": assessment_id,
        "depression_probability": prob_depression,
        "depression_prediction": prediction,
        "risk_level": risk_level,
        "top_factors": top_5_factors,
        "recommendations": recommendations,
        "timestamp": timestamp
    }

@router.get("/history", response_model=list[PredictionResponse])
def get_assessment_history(current_user: dict = Depends(get_current_user)):
    """
    Retrieve previous assessment logs for the authenticated student,
    sorted from most recent to oldest.
    """
    history_col = get_history_collection()
    
    # Query database and sort by timestamp descending
    records = history_col.find(
        {"username": current_user["username"]},
        sort=[("timestamp", -1)]
    )
    
    formatted_records = []
    for r in records:
        # Convert DB documents back to response formats
        formatted_records.append({
            "assessment_id": r["assessment_id"],
            "depression_probability": r["depression_probability"],
            "depression_prediction": r["depression_prediction"],
            "risk_level": r["risk_level"],
            "top_factors": [SHAPFactor(**tf) for tf in r["top_factors"]],
            "recommendations": r["recommendations"],
            "timestamp": r["timestamp"]
        })
        
    return formatted_records
