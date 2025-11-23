#!/bin/bash

# NeuroSmriti - Quick Start Script
# This script automates the complete setup process

set -e  # Exit on error

echo "======================================"
echo "   NeuroSmriti - Quick Start Setup   "
echo "======================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "${BLUE}[1/8] Checking Docker...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker Desktop first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if .env file exists
echo -e "${BLUE}[2/8] Checking environment configuration...${NC}"
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Creating backend/.env from template...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${YELLOW}⚠️  Please edit backend/.env and set a strong SECRET_KEY${NC}"
    echo -e "${YELLOW}   For now, using default values...${NC}"
fi
echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

# Start Docker services
echo -e "${BLUE}[3/8] Starting Docker services...${NC}"
docker-compose down > /dev/null 2>&1 || true
docker-compose up -d
echo -e "${GREEN}✓ Services started (postgres, redis, backend, frontend)${NC}"
echo ""

# Wait for PostgreSQL to be ready
echo -e "${BLUE}[4/8] Waiting for PostgreSQL to be ready...${NC}"
sleep 10
until docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do
    echo "   Waiting for database..."
    sleep 2
done
echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
echo ""

# Load database schema
echo -e "${BLUE}[5/8] Loading database schema...${NC}"
docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI -f /docker-entrypoint-initdb.d/schema.sql > /dev/null 2>&1 || true
echo -e "${GREEN}✓ Schema loaded${NC}"
echo ""

# Load demo data
echo -e "${BLUE}[6/8] Loading demo patient data...${NC}"
cat database/seeds/01_demo_data.sql | docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI > /dev/null 2>&1
echo -e "${GREEN}✓ Demo data loaded (Helen Martinez + 10 memories)${NC}"
echo ""

# Generate synthetic training data
echo -e "${BLUE}[7/8] Generating synthetic training data...${NC}"
if command -v python3 &> /dev/null; then
    cd ml
    if [ ! -d "data/synthetic/train.pkl" ]; then
        echo "   Generating 1000 synthetic patient graphs..."
        python3 scripts/generate_synthetic_data.py > /dev/null 2>&1
        echo -e "${GREEN}✓ Synthetic data generated (train/val/test)${NC}"
    else
        echo -e "${YELLOW}✓ Synthetic data already exists${NC}"
    fi
    cd ..
else
    echo -e "${YELLOW}⚠️  Python3 not found. Skipping synthetic data generation.${NC}"
    echo -e "${YELLOW}   You can run it manually: cd ml && python scripts/generate_synthetic_data.py${NC}"
fi
echo ""

# Display status
echo -e "${BLUE}[8/8] Checking service status...${NC}"
docker-compose ps
echo ""

# Success message
echo -e "${GREEN}======================================"
echo -e "   ✓ Setup Complete! 🎉"
echo -e "======================================${NC}"
echo ""
echo -e "${BLUE}Access your application:${NC}"
echo -e "  • Frontend:        http://localhost:3000"
echo -e "  • API Docs:        http://localhost:8000/docs"
echo -e "  • API Interactive: http://localhost:8000/redoc"
echo ""
echo -e "${BLUE}Demo Login Credentials:${NC}"
echo -e "  • Email:    demo@neurosmriti.com"
echo -e "  • Password: demo123"
echo ""
echo -e "${BLUE}Demo Patient:${NC}"
echo -e "  • Name: Helen Martinez (83 years old)"
echo -e "  • Stage: 2 (Mild Alzheimer's)"
echo -e "  • MMSE Score: 24/30"
echo -e "  • 10 memories with predictions"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Open http://localhost:3000 in your browser"
echo -e "  2. Try the API at http://localhost:8000/docs"
echo -e "  3. Train the ML model:"
echo -e "     cd ml"
echo -e "     jupyter notebook notebooks/02_complete_training.ipynb"
echo ""
echo -e "${YELLOW}Download Real Datasets (Optional):${NC}"
echo -e "  cd ml"
echo -e "  python scripts/download_datasets.py"
echo ""
echo -e "${BLUE}To stop all services:${NC}"
echo -e "  docker-compose down"
echo ""
echo -e "${GREEN}Happy Hacking! 🚀${NC}"
