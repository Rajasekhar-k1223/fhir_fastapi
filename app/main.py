from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import (
    patient_route, practitioner_route, organization_route, allergyIntolerance_route,
    appointment_route, carePlan_route, careTeam_route, condition_route, coverage_route,
    diagnosticReport_route, documentReference_route, encounter_route, episodeCare_route,
    goal_route, immunization_route, medicationRequest_route, observation_route,
    procedure_route, relatedPerson_route,auth
)
from app.core.config import settings
# from PIL import Image

app = FastAPI(title=settings.APP_NAME)

# ✅ Allow CORS for frontend
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://your-frontend.com"  # Replace with actual production URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include FHIR-based routers
app.include_router(auth.router, prefix="/api", tags=["login"])
app.include_router(patient_route.router, prefix="/api", tags=["Patient"])
app.include_router(practitioner_route.router, prefix="/api", tags=["Practitioner"])
app.include_router(organization_route.router, prefix="/api", tags=["Organization"])
app.include_router(allergyIntolerance_route.router, prefix="/api", tags=["Allergy-Intolerance"])
app.include_router(appointment_route.router, prefix="/api", tags=["Appointment"])
app.include_router(carePlan_route.router, prefix="/api", tags=["Care-Plan"])
app.include_router(careTeam_route.router, prefix="/api", tags=["Care-Team"])
app.include_router(coverage_route.router, prefix="/api", tags=["Coverage"])
app.include_router(diagnosticReport_route.router, prefix="/api", tags=["Diagnostic-Report"])
app.include_router(documentReference_route.router, prefix="/api", tags=["Document-Reference"])
app.include_router(encounter_route.router, prefix="/api", tags=["Encounter"])
app.include_router(episodeCare_route.router, prefix="/api", tags=["Episode-of-Care"])
app.include_router(goal_route.router, prefix="/api", tags=["Goal"])
app.include_router(immunization_route.router, prefix="/api", tags=["Immunization"])
app.include_router(medicationRequest_route.router, prefix="/api", tags=["Medication-Request"])
app.include_router(observation_route.router, prefix="/api", tags=["Observation"])
app.include_router(procedure_route.router, prefix="/api", tags=["Procedure"])
app.include_router(relatedPerson_route.router, prefix="/api", tags=["Related-Persons"])
