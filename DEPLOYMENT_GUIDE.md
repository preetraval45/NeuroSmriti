# NeuroSmriti Deployment Guide

**Version**: 2.0
**Last Updated**: December 2024
**Status**: Research Prototype - Not for Clinical Use

---

## ⚠️ Critical Disclaimer

**NeuroSmriti is a RESEARCH PROTOTYPE and educational platform. It is NOT:**
- FDA-approved or CE-marked
- Clinically validated with real patient data
- Intended for medical diagnosis or treatment decisions
- Suitable for deployment in healthcare settings without extensive validation

**DO NOT use this system for actual patient care without:**
1. Clinical validation studies
2. Regulatory approval (FDA, CE, etc.)
3. IRB approval
4. Extensive testing with real data
5. Healthcare professional oversight
6. Continuous monitoring and quality assurance

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Data Preparation](#data-preparation)
5. [Model Training](#model-training)
6. [Deployment](#deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Security & Compliance](#security--compliance)
9. [Troubleshooting](#troubleshooting)

---

## System Overview

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js       │────▶│   FastAPI       │────▶│   PostgreSQL    │
│   Frontend      │     │   Backend       │     │   Database      │
│   (Port 3000)   │     │   (Port 8000)   │     │   (Port 5432)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   ML Models     │
                        │   - MemoryGNN   │
                        │   - Transformer │
                        │   - LSTM        │
                        └─────────────────┘
```

### Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.10+, SQLAlchemy
- **Database**: PostgreSQL 16, Redis 7
- **ML**: PyTorch 2.1, PyTorch Geometric, Transformers
- **Deployment**: Docker, Docker Compose, Nginx

---

## Prerequisites

### Hardware Requirements

**Minimum (Development)**:
- CPU: 4 cores
- RAM: 16 GB
- Storage: 50 GB
- GPU: Not required (CPU training possible)

**Recommended (Production)**:
- CPU: 8+ cores
- RAM: 32+ GB
- Storage: 500 GB SSD
- GPU: NVIDIA with 8+ GB VRAM (for model training/inference)

### Software Requirements

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Node.js**: 18+ (for local development)
- **Python**: 3.10+ (for local development)
- **CUDA**: 11.8+ (if using GPU)

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/NeuroSmriti.git
cd NeuroSmriti
```

### 2. Environment Setup

#### Backend Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
# Database
DATABASE_URL=postgresql://neurosmriti:your_password@db:5432/neurosmriti
POSTGRES_USER=neurosmriti
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=neurosmriti

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=generate_a_secure_random_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_STR=/api/v1
PROJECT_NAME=NeuroSmriti

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

#### Frontend Environment

```bash
cd frontend
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=NeuroSmriti
NEXT_PUBLIC_ENVIRONMENT=development
```

### 3. Docker Deployment

#### Development Mode

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Production Mode

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. Database Initialization

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create initial admin user
docker-compose exec backend python -m app.scripts.create_admin
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (from host)

---

## Data Preparation

### Using Synthetic Data (Default)

The system comes with synthetic data generators:

```bash
cd ml
python data/generate_large_dataset.py
```

This creates 400,000+ synthetic patient records based on clinical research parameters.

### Using Real Clinical Data

**⚠️ Required for clinical deployment**

1. **Download Datasets**: Follow instructions in `ml/data/README_DATA_SOURCES.md`

2. **Organize Data**:
```bash
ml/data/raw/
├── adni/           # ADNI dataset
├── oasis/          # OASIS dataset
├── nacc/           # NACC dataset
└── dementia_bank/  # DementiaBank
```

3. **Check Data Availability**:
```bash
cd ml/data
python real_data_loader.py
```

4. **Preprocess Data**:
```bash
python preprocessing.py --source adni --output processed/
python preprocessing.py --source oasis --output processed/
```

### Data Privacy & Security

- ✓ All data must be de-identified (HIPAA compliance)
- ✓ Use encrypted storage for sensitive data
- ✓ Never commit raw data to version control
- ✓ Follow data use agreements strictly
- ✓ Implement access controls and audit logging

---

## Model Training

### Standard Training

```bash
cd ml/scripts

# Train MemoryGNN
python train_memory_gnn.py

# Train Multimodal Transformer
python train_multimodal.py
```

### Nested Cross-Validation (Recommended)

**For clinical-grade validation with unbiased performance estimates:**

```bash
cd ml/scripts

# 10-fold nested CV with hyperparameter tuning
python train_nested_cv.py
```

This performs:
- **Outer loop**: 10-fold CV for performance estimation
- **Inner loop**: 5-fold CV for hyperparameter tuning
- **Output**: 10 trained models + aggregated metrics with 95% CI

Results saved to: `ml/models/nested_cv_results.json`

### Clinical Validation Metrics

```bash
cd ml/src/evaluation

# Evaluate with clinical metrics
python clinical_metrics.py
```

Calculates:
- Sensitivity, Specificity, Precision, NPV
- AUC-ROC, AUC-PR
- Confidence intervals (Wilson score)
- Cohen's Kappa
- Clinical significance metrics

---

## Deployment

### Local Development

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Celery worker
cd backend
celery -A app.celery_app worker --loglevel=info
```

### Docker Production

```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build --no-cache

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Scale workers
docker-compose -f docker-compose.prod.yml up -d --scale celery-worker=4
```

### Cloud Deployment

#### AWS

```bash
# 1. Create ECS cluster
aws ecs create-cluster --cluster-name neurosmriti-cluster

# 2. Push images to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag neurosmriti-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/neurosmriti-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/neurosmriti-backend:latest

# 3. Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier neurosmriti-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password <secure-password> \
  --allocated-storage 100

# 4. Deploy with ECS/Fargate
aws ecs create-service \
  --cluster neurosmriti-cluster \
  --service-name neurosmriti-backend \
  --task-definition neurosmriti-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

#### Google Cloud Platform

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/<project-id>/neurosmriti-backend

# 2. Deploy to Cloud Run
gcloud run deploy neurosmriti-backend \
  --image gcr.io/<project-id>/neurosmriti-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2
```

#### Azure

```bash
# 1. Create container registry
az acr create --resource-group neurosmriti-rg --name neurosmritiregistry --sku Basic

# 2. Push images
az acr login --name neurosmritiregistry
docker tag neurosmriti-backend neurosmritiregistry.azurecr.io/neurosmriti-backend
docker push neurosmritiregistry.azurecr.io/neurosmriti-backend

# 3. Deploy to Azure Container Instances
az container create \
  --resource-group neurosmriti-rg \
  --name neurosmriti-backend \
  --image neurosmritiregistry.azurecr.io/neurosmriti-backend \
  --cpu 2 \
  --memory 4 \
  --registry-login-server neurosmritiregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --dns-name-label neurosmriti-api
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
docker-compose exec backend python -c "from app.core.database import engine; print(engine.connect())"

# Redis connection
docker-compose exec redis redis-cli ping
```

### Logging

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Export logs
docker-compose logs backend > backend.log
```

### Monitoring Tools

**Recommended Setup**:
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking
- **ELK Stack**: Log aggregation

```bash
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Backup Strategy

#### Database Backup

```bash
# Manual backup
docker-compose exec db pg_dump -U neurosmriti neurosmriti > backup_$(date +%Y%m%d).sql

# Automated daily backups (cron)
0 2 * * * cd /path/to/NeuroSmriti && docker-compose exec -T db pg_dump -U neurosmriti neurosmriti | gzip > backups/db_$(date +\%Y\%m\%d).sql.gz
```

#### Model Backup

```bash
# Backup trained models
tar -czf models_backup_$(date +%Y%m%d).tar.gz ml/models/

# Upload to S3
aws s3 cp models_backup_$(date +%Y%m%d).tar.gz s3://neurosmriti-backups/
```

---

## Security & Compliance

### HIPAA Compliance Checklist

- [ ] All data encrypted at rest (AES-256)
- [ ] All data encrypted in transit (TLS 1.3)
- [ ] Access controls and authentication
- [ ] Audit logging enabled
- [ ] Automatic session timeout
- [ ] Password complexity requirements
- [ ] Business Associate Agreements (BAAs)
- [ ] Incident response plan
- [ ] Regular security audits
- [ ] Data backup and recovery plan

### SSL/TLS Configuration

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Authentication

Enable JWT authentication:

```python
# backend/app/api/v1/auth.py
from fastapi import Depends, HTTPException
from app.core.security import verify_token

@router.post("/login")
async def login(credentials: LoginCredentials):
    user = authenticate_user(credentials)
    if not user:
        raise HTTPException(status_code=401)
    return create_access_token(user.id)
```

---

## Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check if database is running
docker-compose ps

# Check logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up -d db
```

**Model Loading Error**
```bash
# Verify model files exist
ls -lh ml/models/

# Re-train models
cd ml/scripts
python train_nested_cv.py
```

**Frontend Build Error**
```bash
# Clear cache
rm -rf frontend/.next frontend/node_modules

# Reinstall dependencies
cd frontend
npm install

# Rebuild
npm run build
```

**GPU Not Detected**
```bash
# Check CUDA installation
nvidia-smi

# Install CUDA toolkit
# Follow: https://developer.nvidia.com/cuda-toolkit

# Verify PyTorch GPU support
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Performance Optimization

### Database Optimization

```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_patient_id ON predictions(patient_id);
CREATE INDEX idx_created_at ON predictions(created_at);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM patients WHERE ...;
```

### Caching Strategy

```python
# Redis caching for expensive operations
from redis import Redis

redis_client = Redis(host='redis', port=6379, db=0)

def get_prediction(patient_id: int):
    cache_key = f"prediction:{patient_id}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    result = compute_prediction(patient_id)
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return result
```

### Model Optimization

```python
# Convert to ONNX for faster inference
import torch.onnx

torch.onnx.export(
    model,
    dummy_input,
    "model_optimized.onnx",
    opset_version=14,
    do_constant_folding=True
)

# Quantization for reduced model size
import torch.quantization

quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

---

## Support & Resources

### Documentation
- [API Documentation](http://localhost:8000/docs)
- [Developer Guide](./DEVELOPER_GUIDE.md)
- [Data Sources Guide](./ml/data/README_DATA_SOURCES.md)

### Research References
- ADNI: https://adni.loni.usc.edu/
- OASIS: https://www.oasis-brains.org/
- Alzheimer's Association: https://www.alz.org/

### Getting Help
- GitHub Issues: [Report bugs or request features]
- Email: support@neurosmriti.com
- Slack: [Developer community]

---

## License & Citation

### License
MIT License - See LICENSE file

### Citation
If you use NeuroSmriti in your research, please cite:

```bibtex
@software{neurosmriti2024,
  title={NeuroSmriti: AI-Powered Alzheimer's Detection Platform},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/NeuroSmriti}
}
```

---

**Last Updated**: December 2024
**Version**: 2.0
**Maintainer**: NeuroSmriti Development Team
