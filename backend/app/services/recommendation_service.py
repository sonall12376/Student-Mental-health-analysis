from app.models.schemas import AssessmentInput
from typing import List

def generate_personalized_recommendations(assessment: AssessmentInput, risk_level: str) -> List[str]:
    """
    Generate personalized recommendations based on the student's assessment answers
    and predicted risk level.
    """
    recommendations = []
    
    # 1. Critical Crisis Intervention (Highest Priority)
    if assessment.have_you_ever_had_suicidal_thoughts.strip().lower() == "yes":
        recommendations.append(
            "CRITICAL: We noticed you indicated a history of suicidal thoughts. Please know that you are not alone, "
            "and professional support is available. We strongly urge you to contact the Suicide & Crisis Lifeline "
            "by calling or texting 988 (available 24/7, free and confidential) or reach out to your campus counseling center immediately."
        )
        
    # 2. Risk Level Specific Guidance
    if risk_level == "High":
        recommendations.append(
            "Recommended Action: Schedule a visit with a mental health professional or student counselor. "
            "Our analysis indicates high levels of current mental strain, and a professional can help you navigate this securely."
        )
    elif risk_level == "Moderate":
        recommendations.append(
            "Recommended Action: Reach out to campus peer-support groups or attend student stress-management workshops. "
            "Consider talking to a trusted friend or mentor about how you're feeling."
        )
    else:
        recommendations.append(
            "Recommended Action: Maintain your healthy routine! Practice daily mindfulness and continue prioritizing your self-care."
        )
        
    # 3. Feature-Specific Guidance
    # Sleep
    sleep_val = assessment.sleep_duration.strip()
    if sleep_val in ["Less than 5 hours", "Irregular Sleep"]:
        recommendations.append(
            "Sleep Hygiene: Your sleep duration is low or irregular. Prioritize 7-8 hours of sleep. "
            "Establish a consistent sleep schedule and avoid screens (phone/laptop) at least 30 minutes before bed."
        )
    elif sleep_val == "5-6 hours":
        recommendations.append(
            "Sleep Tip: Try increasing your sleep time by 30-60 minutes. Minor increases in deep sleep "
            "significantly improve focus, cognitive performance, and emotional resilience."
        )
        
    # Diet
    diet_val = assessment.dietary_habits.strip()
    if diet_val in ["Unhealthy", "Irregular Diet"]:
        recommendations.append(
            "Nutritional Tip: Irregular or unhealthy diet habits can disrupt the gut-brain axis, worsening mood drops. "
            "Try eating at regular intervals, stay hydrated, and include raw fruits, vegetables, and proteins in your meals."
        )
        
    # Academic Pressure
    if assessment.academic_pressure >= 4:
        recommendations.append(
            "Academic Management: High academic load is taxing your mental reserve. Try using the Pomodoro Technique "
            "(study for 25 minutes, break for 5 minutes) to avoid cognitive fatigue, and break large projects into tiny, manageable sub-tasks."
        )
        
    # Financial Stress
    if assessment.financial_stress >= 4:
        recommendations.append(
            "Financial Resources: Financial anxiety is a massive burden. Check with your university's student union "
            "or financial aid office for emergency stipends, budgeting workshops, work-study programs, or hardship scholarships."
        )
        
    # Study Satisfaction
    if assessment.study_satisfaction <= 2:
        recommendations.append(
            "Course Alignment: Low interest in your course is a primary driver of academic burnout. "
            "Schedule a session with an academic advisor to discuss elective swaps or major changes that align better with your interests."
        )
        
    # Work/Study Hours
    if assessment.work_study_hours >= 10:
        recommendations.append(
            "Workload Boundary: You are spending over 10 hours daily studying or working. "
            "Create a strict cutoff time in the evening (e.g. 8:00 PM) where all work shuts down, allowing your brain time to fully recharge."
        )
        
    # 4. General Well-being Add-on
    if len(recommendations) < 3:
        recommendations.append(
            "General Well-being: Incorporate 20-30 minutes of light exercise (like walking or yoga) into your daily routine. "
            "Physical movement naturally releases endorphins, lowering baseline stress."
        )
        
    return recommendations
