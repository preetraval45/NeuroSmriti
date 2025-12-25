"""
NeuroSmriti - Main FastAPI Application
Cognitive Digital Twin for Alzheimer's Care
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import (
    auth, patients, predictions, memories, interventions, cognitive_tests,
    ml_advanced, advanced_features, communication, safety,
    clinical_support, research_data, social_gamification, integrations
)

# Create database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered platform for Alzheimer's detection, prediction, and daily living support",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (security)
if settings.ENVIRONMENT == "production":
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with timing"""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {process_time:.3f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time()
    }


@app.get("/api/health")
async def api_health_check():
    """API health check"""
    # TODO: Add database connection check
    # TODO: Add Redis connection check
    # TODO: Add ML model loading check
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "ml_models": "loaded"
    }


# Include API routers
API_V1_PREFIX = "/api/v1"

# Core routers
app.include_router(auth.router, prefix=f"{API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(patients.router, prefix=f"{API_V1_PREFIX}/patients", tags=["Patients"])
app.include_router(predictions.router, prefix=f"{API_V1_PREFIX}/predictions", tags=["AI Predictions"])
app.include_router(memories.router, prefix=f"{API_V1_PREFIX}/memories", tags=["Memory Graph"])
app.include_router(interventions.router, prefix=f"{API_V1_PREFIX}/interventions", tags=["Interventions"])
app.include_router(cognitive_tests.router, prefix=f"{API_V1_PREFIX}/cognitive-tests", tags=["Cognitive Tests"])

# Advanced ML & AI routers
app.include_router(ml_advanced.router, prefix=API_V1_PREFIX, tags=["Advanced ML"])
app.include_router(advanced_features.router, prefix=API_V1_PREFIX, tags=["Advanced AI Features"])

# Communication & Safety routers
app.include_router(communication.router, prefix=API_V1_PREFIX, tags=["Communication"])
app.include_router(safety.router, prefix=API_V1_PREFIX, tags=["Safety & Monitoring"])

# Clinical Decision Support & Research routers
app.include_router(clinical_support.router, prefix=API_V1_PREFIX, tags=["Clinical Decision Support"])
app.include_router(research_data.router, prefix=API_V1_PREFIX, tags=["Research & Data"])

# Social & Gamification routers
app.include_router(social_gamification.router, prefix=API_V1_PREFIX, tags=["Social & Gamification"])

# Integration routers
app.include_router(integrations.router, prefix=API_V1_PREFIX, tags=["Integration & Automation"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # TODO: Initialize ML models
    # TODO: Connect to database
    # TODO: Connect to Redis
    logger.info("Application startup complete")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down application...")
    # TODO: Close database connections
    # TODO: Close Redis connections
    # TODO: Save any pending data
    logger.info("Shutdown complete")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
