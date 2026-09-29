from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# ==========================================
# Auth Schemas
# ==========================================
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    password: str = Field(..., min_length=6, example="password123")
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    age: int = Field(..., ge=15, le=100, example=21)
    gender: str = Field(..., example="Male")

class UserLogin(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="password123")

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    name: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ==========================================
# Assessment Schemas
# ==========================================
class AssessmentInput(BaseModel):
    gender: str = Field(..., description="Gender (Male/Female)")
    age: int = Field(..., ge=18, le=60, description="Age of the student")
    academic_pressure: int = Field(..., ge=0, le=5, description="Academic pressure rating (0-5)")
    cgpa: float = Field(..., ge=0.0, le=10.0, description="CGPA (0.0 to 10.0)")
    study_satisfaction: int = Field(..., ge=0, le=5, description="Study satisfaction rating (0-5)")
    sleep_duration: str = Field(..., description="Typical sleep hours per night")
    dietary_habits: str = Field(..., description="Dietary quality habits")
    degree: str = Field(..., description="Academic degree program")
    have_you_ever_had_suicidal_thoughts: str = Field(..., description="Suicidal ideation history (Yes/No)")
    work_study_hours: int = Field(..., ge=0, le=12, description="Daily study/work workload hours")
    financial_stress: int = Field(..., ge=1, le=5, description="Financial stress rating (1-5)")
    family_history_of_mental_illness: str = Field(..., description="Family mental health history (Yes/No)")

class SHAPFactor(BaseModel):
    feature: str
    feature_value: float
    shap_value: float
    description: str  # Student-friendly explanation of this specific factor

class PredictionResponse(BaseModel):
    assessment_id: str
    depression_probability: float
    depression_prediction: int
    risk_level: str
    top_factors: List[SHAPFactor]
    recommendations: List[str]
    timestamp: str

class ExplanationRequest(BaseModel):
    assessment: AssessmentInput

class ExplanationResponse(BaseModel):
    attributions: List[SHAPFactor]

class RecommendationRequest(BaseModel):
    assessment: AssessmentInput
    risk_level: str

class RecommendationResponse(BaseModel):
    recommendations: List[str]

# ==========================================
# History Schemas
# ==========================================
class HistoryRecord(BaseModel):
    assessment_id: str
    username: str
    input_data: AssessmentInput
    depression_probability: float
    depression_prediction: int
    risk_level: str
    timestamp: str
