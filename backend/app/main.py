from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, predict, explain, recommend
from app.database import database_status

# Initialize FastAPI application
app = FastAPI(
    title="MindEase | AI Student Depression Risk Predictor & Recommender API",
    description="Backend API for predicting student depression risk, providing SHAP explanations, and rendering personalized recommendations.",
    version="1.0.0"
)

# Configure CORS Middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(predict.router)  # Register predict at root to expose POST /predict and GET /history directly
app.include_router(explain.router)
app.include_router(recommend.router)

@app.get("/")
def read_root():
    """
    Root endpoint to verify backend status and database type.
    """
    db_status = database_status()
    return {
        "message": "Welcome to the MindEase Student Depression Risk Prediction API!",
        "status": "online",
        "database": db_status,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    # Run the server on localhost:8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
