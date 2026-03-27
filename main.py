from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database import Base, engine
from routers import auth, users, feedback, video_calls, jobs, training, assessments, career, ai

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inclusive Feedback Platform API",
    description="Backend for the Inclusive professional development and feedback platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(feedback.router)
app.include_router(video_calls.router)
app.include_router(jobs.router)
app.include_router(training.router)
app.include_router(assessments.router)
app.include_router(career.router)
app.include_router(ai.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}
