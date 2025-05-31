from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import patient_route
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

# ✅ Allow CORS for development and production
origins = [
    "http://localhost:4200",     # React dev server
    "http://127.0.0.1:4200",     # Localhost
    "https://your-frontend.com"  # Replace with your production frontend domain
]

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # You can also use ["*"] for all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(patient_route.router, prefix="/api", tags=["Patient"])
