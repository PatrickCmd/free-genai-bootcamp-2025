from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.words import router as words_router

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