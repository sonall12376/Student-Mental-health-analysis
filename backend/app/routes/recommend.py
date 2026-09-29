from fastapi import APIRouter
from app.models.schemas import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import generate_personalized_recommendations

router = APIRouter(prefix="/recommend", tags=["Recommendation Engine"])

@router.post("", response_model=RecommendationResponse)
def get_recommendations(payload: RecommendationRequest):
    """
    Generate targeted student well-being and academic recommendations
    for a given assessment input and predicted risk level.
    """
    recommendations = generate_personalized_recommendations(payload.assessment, payload.risk_level)
    return {
        "recommendations": recommendations
    }
