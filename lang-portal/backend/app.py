from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.words import router as words_router
from routes.groups import router as groups_router
from routes.study_activities import router as study_activities_router
from routes.study_sessions import router as study_sessions_router
from routes.dashboard import router as dashboard_router
from routes.reset import router as reset_router

app = FastAPI(
    title="Language Portal API",
    description="API for managing language learning resources",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(words_router, prefix="/api")
app.include_router(groups_router, prefix="/api")
app.include_router(study_activities_router, prefix="/api")
app.include_router(study_sessions_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(reset_router, prefix="/api") 