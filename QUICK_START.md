# NeuroSmriti - Quick Start Guide

Get your entire project running in **under 5 minutes** with a single command!

## Prerequisites

- **Docker Desktop** installed and running
- **Git** installed (to clone the repo)
- **Python 3.8+** (optional, for ML training)

## 🚀 Fastest Way to Start

### For Windows Users:

```bash
# Just double-click the file in Windows Explorer
quick_start.bat

# OR run from PowerShell/CMD
.\quick_start.bat
```

### For Linux/Mac Users:

```bash
# Make it executable
chmod +x quick_start.sh

# Run it
./quick_start.sh
```

## What Does the Quick Start Script Do?

The script automatically handles everything:

1. ✅ **Checks Docker** - Ensures Docker Desktop is running
2. ✅ **Creates .env file** - Copies backend/.env.example to backend/.env
3. ✅ **Starts services** - Launches postgres, redis, backend, frontend via docker-compose
4. ✅ **Initializes database** - Creates tables, indexes, constraints
5. ✅ **Loads demo data** - Adds Helen Martinez (demo patient) with 10 memories
6. ✅ **Generates training data** - Creates 1000 synthetic patient graphs
7. ✅ **Verifies services** - Shows status of all running containers
8. ✅ **Displays access info** - Shows URLs and login credentials

**Total Time: ~2-3 minutes** (depending on your internet speed for Docker images)

## 📱 Access Your Application

Once the script completes, you'll see:

```
======================================
   ✓ Setup Complete! 🎉
======================================

Access your application:
  • Frontend:        http://localhost:3000
  • API Docs:        http://localhost:8000/docs
  • API Interactive: http://localhost:8000/redoc

Demo Login Credentials:
  • Email:    demo@neurosmriti.com
  • Password: demo123

Demo Patient:
  • Name: Helen Martinez (83 years old)
  • Stage: 2 (Mild Alzheimer's)
  • MMSE Score: 24/30
  • 10 memories with predictions
```

### Test the API

1. Open [http://localhost:8000/docs](http://localhost:8000/docs)
2. Click **"Authorize"** button (top right)
3. Use credentials:
   - **username**: `demo@neurosmriti.com`
   - **password**: `demo123`
4. Try these endpoints:
   - `GET /api/v1/patients/` - List all patients
   - `GET /api/v1/patients/{id}/memories` - View Helen's memories
   - `GET /api/v1/patients/{id}/predictions` - See decay predictions

### Test the Frontend

1. Open [http://localhost:3000](http://localhost:3000)
2. You'll see the landing page with "NeuroSmriti" hero section
3. Click "Get Started" or navigate to `/login`
4. Login with demo credentials
5. View Helen Martinez's memory dashboard

## 🧠 Train the ML Model

### Using Jupyter Notebook (Recommended):

```bash
cd ml

# Install Jupyter if not already installed
pip install jupyter matplotlib seaborn

# Start Jupyter
jupyter notebook notebooks/02_complete_training.ipynb

# In Jupyter: Cell → Run All
```

The notebook will:
- Load the 1000 synthetic patient graphs
- Train MemoryGNN for 50 epochs (with early stopping)
- Display training curves and metrics
- Save the best model to `ml/models/memory_gnn_best.pth`
- Copy model to `backend/app/ml/models/` for production

**Expected Results:**
- Training Accuracy: 91-93%
- Test Accuracy: 88-90%
- Training Time: ~5-10 minutes (CPU) or ~2-3 minutes (GPU)

### Using Python Script:

```bash
cd ml
python scripts/train_memory_gnn.py
```

## 📊 Download Real Datasets (Optional)

To train on real Alzheimer's data instead of synthetic:

```bash
cd ml
python scripts/download_datasets.py
```

This will guide you to download from:
- **Hack4Health Dataset** - Google Drive (provided by hackathon)
- **OASIS Dataset** - ~2GB, free, no registration
- **Kaggle Datasets** - Requires Kaggle account

Then re-run the training notebook - it will automatically detect and use real data.

## 🛠️ Manual Setup (If Script Fails)

If the quick start script doesn't work, follow these manual steps:

### Step 1: Create Environment File

```bash
cp backend/.env.example backend/.env

# Edit backend/.env and set a strong SECRET_KEY:
# SECRET_KEY=your-very-long-secret-key-minimum-32-characters
```

### Step 2: Start Docker Services

```bash
docker-compose up -d
```

### Step 3: Wait for Database (10 seconds)

```bash
# Windows
timeout /t 10

# Linux/Mac
sleep 10
```

### Step 4: Load Database Schema

```bash
docker-compose exec postgres psql -U postgres -d NEUROSMRITI -f /docker-entrypoint-initdb.d/schema.sql
```

### Step 5: Load Demo Data

```bash
# Windows
type database\seeds\01_demo_data.sql | docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI

# Linux/Mac
cat database/seeds/01_demo_data.sql | docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI
```

### Step 6: Generate Synthetic Data

```bash
cd ml
python scripts/generate_synthetic_data.py
```

## 🔧 Troubleshooting

### Issue: "Docker is not running"

**Solution:**
1. Open Docker Desktop
2. Wait for it to fully start (green light in system tray)
3. Run the quick start script again

### Issue: "Port already in use"

**Solution:**
```bash
# Stop all running containers
docker-compose down

# Kill any processes using the ports
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Start again
docker-compose up -d
```

### Issue: "Database not found"

**Solution:**
```bash
# Check if database exists
docker-compose exec postgres psql -U postgres -c "\l"

# You should see NEUROSMRITI in the list
# If not, recreate it:
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE NEUROSMRITI;"
```

### Issue: "Demo data not loading"

**Solution:**
```bash
# Check if users table has data
docker-compose exec postgres psql -U postgres -d NEUROSMRITI -c "SELECT * FROM users;"

# If empty, reload:
cat database/seeds/01_demo_data.sql | docker-compose exec -T postgres psql -U postgres -d NEUROSMRITI
```

### Issue: "Frontend not loading"

**Solution:**
```bash
# Check container logs
docker-compose logs frontend

# Restart frontend container
docker-compose restart frontend

# Rebuild if needed
docker-compose up -d --build frontend
```

## 📝 Verify Everything Works

Run these commands to verify your setup:

```bash
# Check all containers are running
docker-compose ps

# Expected output:
# neurosmriti-postgres    running
# neurosmriti-redis       running
# neurosmriti-backend     running
# neurosmriti-frontend    running

# Check backend API health
curl http://localhost:8000/health

# Check frontend is serving
curl http://localhost:3000

# Check database has data
docker-compose exec postgres psql -U postgres -d NEUROSMRITI -c "SELECT full_name FROM patients;"

# Expected output: Helen Martinez

# Check synthetic data exists
ls ml/data/synthetic/

# Expected output: train.pkl  val.pkl  test.pkl
```

## 🎯 Next Steps After Setup

### For Hackathon Demo:

1. **Build the Frontend Dashboard** (~2 hours)
   - Patient list page
   - Memory graph visualization (D3.js)
   - Risk dashboard

2. **Record Demo Video** (~30 minutes)
   - Show Helen's memory graph
   - Demonstrate predictions
   - Show intervention recommendations

3. **Write Project Report** (~1 hour)
   - Problem statement
   - Solution approach
   - Technical architecture
   - Results and impact

### For Development:

1. **Add more API endpoints**
   - `POST /api/v1/memories` - Add new memory
   - `PUT /api/v1/memories/{id}` - Update memory
   - `GET /api/v1/interventions` - Get intervention recommendations

2. **Build React components**
   - `PatientCard.tsx`
   - `MemoryGraph.tsx`
   - `RiskDashboard.tsx`
   - `InterventionList.tsx`

3. **Improve ML model**
   - Add multimodal fusion (MRI + cognitive + speech)
   - Implement attention visualization
   - Add explainable AI features

## 📚 Useful Commands

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Restart a service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Connect to database
docker-compose exec postgres psql -U postgres -d NEUROSMRITI

# Run Django/Flask-like shell
docker-compose exec backend python -c "from app.core.database import SessionLocal; db = SessionLocal(); print('DB connected!')"
```

## 🌐 Database Connection (External Tools)

If you want to connect pgAdmin, DBeaver, or another DB tool:

```
Host:     localhost
Port:     5432
Database: NEUROSMRITI
Username: postgres
Password: postgres
```

**Connection String:**
```
postgresql://postgres:postgres@localhost:5432/NEUROSMRITI
```

## 🎉 You're All Set!

Your NeuroSmriti project is now fully running and ready for development!

**What you have:**
- ✅ Backend API with authentication
- ✅ Frontend with Next.js and Tailwind
- ✅ PostgreSQL database with demo data
- ✅ Redis for caching
- ✅ ML training pipeline with synthetic data
- ✅ Complete documentation

**Ready for:**
- ✅ Building the dashboard UI
- ✅ Training ML models
- ✅ Adding new features
- ✅ Creating hackathon demo
- ✅ Impressing judges and boosting your resume

**Need Help?**
- Check [GETTING_STARTED.md](GETTING_STARTED.md) for detailed guides
- See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for codebase overview
- Read [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) for ML training
- Review [PRODUCT_IMPROVEMENTS.md](PRODUCT_IMPROVEMENTS.md) for ideas

**Happy Building! 🚀**
