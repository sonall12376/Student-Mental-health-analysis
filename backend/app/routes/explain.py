import pandas as pd
from fastapi import APIRouter, Depends
from app.models.schemas import ExplanationRequest, ExplanationResponse, SHAPFactor
from app.routes.predict import get_features, get_explainer, KEY_MAPPING, get_feature_description
from app.utils.preprocess import preprocess_features

router = APIRouter(prefix="/explain", tags=["Explainable AI"])

@router.post("", response_model=ExplanationResponse)
def explain_prediction(payload: ExplanationRequest):
    """
    Generate SHAP Shapley attribution explanations for a given student assessment input profile.
    This does not save the profile to database history.
    """
    features = get_features()
    explainer = get_explainer()
    
    # 1. Translate keys
    raw_dict = {}
    assessment_dict = payload.assessment.model_dump()
    for snake_k, raw_k in KEY_MAPPING.items():
        raw_dict[raw_k] = assessment_dict[snake_k]
        
    # 2. Convert to DataFrame
    raw_df = pd.DataFrame([raw_dict])
    
    # 3. Preprocess
    preprocessed_df = preprocess_features(raw_df, trained_columns=features)
    
    # 4. Calculate SHAP values
    shap_output = explainer(preprocessed_df)
    shap_vals = shap_output[0].values
    
    # 5. Format SHAP attributions
    attributions = []
    for feat_name, sv, fv in zip(features, shap_vals, shap_output[0].data):
        # Exclude inactive degree columns
        if feat_name.startswith("Degree_") and fv == 0:
            continue
            
        desc = get_feature_description(feat_name, sv)
        attributions.append(SHAPFactor(
            feature=feat_name,
            feature_value=float(fv),
            shap_value=float(sv),
            description=desc
        ))
        
    # Sort by absolute SHAP value (impact) descending
    attributions.sort(key=lambda x: abs(x.shap_value), reverse=True)
    
    return {
        "attributions": attributions
    }
