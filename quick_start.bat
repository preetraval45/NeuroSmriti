@echo off
REM NeuroSmriti - Quick Start Script for Windows
REM This script automates the complete setup process

echo ======================================
echo    NeuroSmriti - Quick Start Setup
echo ======================================
echo.

REM Check if Docker is running
echo [1/8] Checking Docker...
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is running
echo.

REM Check if .env file exists
echo [2/8] Checking environment configuration...
if not exist "backend\.env" (
    echo Creating backend\.env from template...
    copy "backend\.env.example" "backend\.env" >nul
    echo Warning: Please edit backend\.env and set a strong SECRET_KEY
    echo For now, using default values...
)
echo [OK] Environment configured
echo.

REM Start Docker services
echo [3/8] Starting Docker services...
docker-compose down >nul 2>&1
docker-compose up -d
echo [OK] Services started (postgres, redis, backend, frontend)
echo.

REM Wait for PostgreSQL to be ready
echo [4/8] Waiting for PostgreSQL to be ready...
timeout /t 10 /nobreak >nul
:wait_for_postgres
docker-compose exec -T postgres pg_isready -U postgres >nul 2>&1
if errorlevel 1 (
    echo    Waiting for database...
    timeout /t 2 /nobreak >nul
    goto wait_for_postgres
)
echo [OK] PostgreSQL is ready
echo.

REM Load database schema
echo [5/8] Loading database schema...
docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI -f /docker-entrypoint-initdb.d/schema.sql >nul 2>&1
echo [OK] Schema loaded
echo.

REM Load demo data
echo [6/8] Loading demo patient data...
type "database\seeds\01_demo_data.sql" | docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI >nul 2>&1
echo [OK] Demo data loaded (Helen Martinez + 10 memories)
echo.

REM Generate synthetic training data
echo [7/8] Generating synthetic training data...
where python >nul 2>&1
if errorlevel 1 (
    echo Warning: Python not found. Skipping synthetic data generation.
    echo You can run it manually: cd ml ^&^& python scripts\generate_synthetic_data.py
) else (
    if not exist "ml\data\synthetic\train.pkl" (
        echo    Generating 1000 synthetic patient graphs...
        cd ml
        python scripts\generate_synthetic_data.py >nul 2>&1
        cd ..
        echo [OK] Synthetic data generated (train/val/test)
    ) else (
        echo [OK] Synthetic data already exists
    )
)
echo.

REM Display status
echo [8/8] Checking service status...
docker-compose ps
echo.

REM Success message
echo ======================================
echo    [OK] Setup Complete! 🎉
echo ======================================
echo.
echo Access your application:
echo   • Frontend:        http://localhost:3000
echo   • API Docs:        http://localhost:8000/docs
echo   • API Interactive: http://localhost:8000/redoc
echo.
echo Demo Login Credentials:
echo   • Email:    demo@neurosmriti.com
echo   • Password: demo123
echo.
echo Demo Patient:
echo   • Name: Helen Martinez (83 years old)
echo   • Stage: 2 (Mild Alzheimer's)
echo   • MMSE Score: 24/30
echo   • 10 memories with predictions
echo.
echo Next Steps:
echo   1. Open http://localhost:3000 in your browser
echo   2. Try the API at http://localhost:8000/docs
echo   3. Train the ML model:
echo      cd ml
echo      jupyter notebook notebooks\02_complete_training.ipynb
echo.
echo Download Real Datasets (Optional):
echo   cd ml
echo   python scripts\download_datasets.py
echo.
echo To stop all services:
echo   docker-compose down
echo.
echo Happy Hacking! 🚀
echo.
pause
