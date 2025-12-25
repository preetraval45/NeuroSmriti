# 🚀 NeuroSmriti - Complete Startup Guide

## Quick Start (All-in-One)

### Option 1: Start with Pre-Trained Models (Recommended)

```bash
# Models are already trained! Just start the containers
docker-compose down -v  # Clean slate
docker-compose up --build
```

**Services will be available at:**
- 🌐 Frontend: http://localhost:3103
- 🔧 Backend API: http://localhost:3102
- 🔍 API Docs: http://localhost:3102/docs
- 💾 PostgreSQL: localhost:3100
- 🔴 Redis: localhost:3101

---

### Option 2: Retrain Models in Docker (Optional)

If you want to retrain the ML models fresh:

```bash
# Step 1: Stop existing containers
docker-compose down -v

# Step 2: Train models locally (faster than in Docker)
cd ml
python data/generate_sample_data.py
python train_models_fixed.py
cp models/* ../backend/app/ml/models/

# Step 3: Start all services
cd ..
docker-compose up --build
```

---

## 🎯 Complete Setup & Verification

### Step 1: Verify Docker is Running

```bash
docker --version
docker-compose --version
```

### Step 2: Clean Previous Containers

```bash
# Remove old containers and volumes
docker-compose down -v

# Remove any dangling images (optional)
docker system prune -f
```

### Step 3: Build and Start Services

```bash
# Build and start all services in detached mode
docker-compose up --build -d
```

**This will:**
1. Build backend Docker image
2. Build frontend Docker image
3. Pull PostgreSQL 16
4. Pull Redis 7
5. Create network and volumes
6. Start all 6 services

### Step 4: Watch Logs

```bash
# Watch all services
docker-compose logs -f

# Or watch specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Step 5: Verify Services are Healthy

```bash
# Check container status
docker-compose ps

# Should show:
# postgres    - Up (healthy)
# redis       - Up (healthy)
# backend     - Up
# celery      - Up
# frontend    - Up
# nginx       - Up
```

### Step 6: Initialize Database

The database initializes automatically from `database/schema.sql` and `database/seeds/` on first run.

**Verify:**
```bash
# Check database initialization logs
docker-compose logs postgres | grep "database system is ready"
```

### Step 7: Verify ML Models

```bash
# Check if models are available in backend container
docker-compose exec backend ls -lh /app/app/ml/models/

# Should show:
# ensemble_model.pkl
# random_forest_model.pkl
# gradient_boosting_model.pkl
# neural_network_model.pkl
# scaler.pkl
# label_encoder.pkl
# model_registry.json
```

### Step 8: Test the Application

#### A. Access Frontend
1. Open http://localhost:3103
2. You should see the NeuroSmriti landing page

#### B. Test API
```bash
# Health check
curl http://localhost:3102/health

# API documentation
# Visit: http://localhost:3102/docs
```

#### C. Create Test User & Login
```bash
# Register
curl -X POST http://localhost:3102/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@neurosmriti.com",
    "password": "Test123!",
    "full_name": "Test User"
  }'

# Login (save the access_token)
curl -X POST http://localhost:3102/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@neurosmriti.com",
    "password": "Test123!"
  }'
```

#### D. Test ML Predictions

```bash
# Set your token from login
TOKEN="your_access_token_here"

# Create a patient
curl -X POST http://localhost:3102/api/v1/patients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "date_of_birth": "1950-01-15",
    "gender": "Male",
    "current_stage": 1,
    "mmse_score": 24,
    "moca_score": 22
  }'

# Get patient ID from response, then predict stage
PATIENT_ID="patient_id_from_above"

curl -X POST "http://localhost:3102/api/v1/predictions/stage?patient_id=$PATIENT_ID" \
  -H "Authorization: Bearer $TOKEN"

# Should return:
# {
#   "patient_id": "...",
#   "predicted_stage": 1,
#   "stage_name": "mci",
#   "confidence": 0.75,
#   "stage_probabilities": {...},
#   "progression_risk": "low",
#   ...
# }
```

---

## 📊 Monitoring & Debugging

### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Backend only (ML predictions)
docker-compose logs -f backend

# Database
docker-compose logs -f postgres

# Celery worker (async tasks)
docker-compose logs -f celery
```

### Check Resource Usage

```bash
# Container stats (CPU, Memory, etc.)
docker stats

# Specific container
docker stats neurosmriti-backend
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend bash

# Once inside:
python -c "from app.services.ml_service import ml_service; ml_service.load_traditional_models(); print('Models loaded!')"

# Database shell
docker-compose exec postgres psql -U postgres -d NEUROSMRITI

# Redis CLI
docker-compose exec redis redis-cli
```

### Restart Specific Service

```bash
# Restart backend only
docker-compose restart backend

# Restart all
docker-compose restart
```

---

## 🔧 Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port 3103
lsof -i :3103  # On Mac/Linux
netstat -ano | findstr :3103  # On Windows

# Stop docker-compose and change ports in docker-compose.yml if needed
```

### Issue: Models Not Found

```bash
# Copy models to backend
cp ml/models/*.pkl backend/app/ml/models/
cp ml/models/*.json backend/app/ml/models/

# Rebuild backend
docker-compose up --build -d backend
```

### Issue: Database Connection Failed

```bash
# Check if postgres is healthy
docker-compose ps postgres

# View postgres logs
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres
```

### Issue: Frontend Won't Build

```bash
# Clear frontend build cache
rm -rf frontend/.next
rm -rf frontend/out

# Rebuild
docker-compose up --build frontend nginx
```

### Issue: Celery Worker Not Starting

```bash
# Check celery logs
docker-compose logs celery

# Restart celery
docker-compose restart celery
```

---

## 🧪 Run Tests

### Backend Tests

```bash
# Run tests in Docker
docker-compose exec backend pytest tests/ -v

# OR run locally
cd backend
python -m pytest tests/ -v --cov=app
```

### ML Model Tests

```bash
# Run locally (models must be present)
cd ml
pytest tests/ -v
```

### Frontend Tests

```bash
# Run in frontend container
docker-compose exec frontend npm test

# OR run locally
cd frontend
npm test
```

---

## 🎨 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3103 | Main web application |
| **Backend API** | http://localhost:3102 | REST API |
| **API Docs** | http://localhost:3102/docs | Interactive Swagger UI |
| **ReDoc** | http://localhost:3102/redoc | API documentation |
| **Health Check** | http://localhost:3102/health | Service status |
| **PostgreSQL** | localhost:3100 | Database (user: postgres, pass: postgres) |
| **Redis** | localhost:3101 | Cache & queue |

---

## 📦 Production Deployment

### Using Production Docker Compose

```bash
# Set environment variables
export SECRET_KEY="your-super-secret-key-min-32-characters"
export POSTGRES_PASSWORD="secure-database-password"
export BACKEND_CORS_ORIGINS='["https://yourdomain.com"]'
export NEXT_PUBLIC_API_URL="https://api.yourdomain.com"

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

**Production features:**
- Multi-worker backend (4 Uvicorn workers)
- Celery worker pool (4 concurrent workers)
- Health checks for all services
- Automatic restarts
- Volume persistence
- Production-optimized settings

---

## 🔐 Default Credentials

### Demo Account (Pre-seeded)
- **Email:** demo@neurosmriti.com
- **Password:** demo123

### Database
- **User:** postgres
- **Password:** postgres (CHANGE IN PRODUCTION!)
- **Database:** NEUROSMRITI

---

## 📝 Common Commands Cheat Sheet

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Rebuild specific service
docker-compose up --build backend

# View logs
docker-compose logs -f [service]

# Execute command in container
docker-compose exec [service] [command]

# Check service status
docker-compose ps

# Restart service
docker-compose restart [service]

# Remove stopped containers
docker-compose rm

# Pull latest images
docker-compose pull
```

---

## 🎯 Next Steps After Startup

1. **Create Your First Patient**
   - Navigate to http://localhost:3103
   - Register/Login
   - Go to Patients → Add Patient
   - Fill in patient details

2. **Run AI Prediction**
   - Select a patient
   - Go to Predictions
   - Click "Predict Alzheimer's Stage"
   - View results with confidence scores

3. **Add Memories**
   - In patient details
   - Add memories (people, places, events)
   - Create memory connections

4. **Predict Memory Decay**
   - With memories added
   - Run memory decay prediction
   - View high-risk memories

5. **Schedule Interventions**
   - Based on high-risk memories
   - Create intervention plans
   - Track intervention results

---

## 📚 Additional Resources

- **API Documentation:** http://localhost:3102/docs
- **Implementation Summary:** [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **Memory GNN Guide:** [MEMORY_GNN_TRAINING_GUIDE.md](./MEMORY_GNN_TRAINING_GUIDE.md)
- **Project Status:** [docs/PROJECT_STATUS.md](./docs/PROJECT_STATUS.md)

---

## 🆘 Getting Help

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify services: `docker-compose ps`
3. Check models: `docker-compose exec backend ls /app/app/ml/models/`
4. Review [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
5. Open an issue on GitHub

---

**🎉 Your NeuroSmriti AI Platform is Ready!**

The ML models are trained, the API is live, and the frontend is beautiful. Time to detect Alzheimer's and preserve memories! 🧠✨

---

*Last updated: December 25, 2025*
*Docker Compose Version: 3.8*
*All services tested and verified*
