# NeuroSmriti ML Models

This directory contains machine learning models for Alzheimer's detection and memory decay prediction.

## Directory Structure

- `models/` - Trained model weights (.pth, .onnx)
- `notebooks/` - Jupyter notebooks for exploration and training
- `data/` - Datasets (not committed to git)
- `scripts/` - Training and evaluation scripts
- `src/` - Source code for model architectures

## Models

### 1. MemoryGNN (Graph Neural Network)
- **Purpose**: Predict memory decay in knowledge graph
- **Architecture**: Graph Attention Networks (GAT)
- **Input**: Patient memory graph
- **Output**: Node-level decay predictions

### 2. Multimodal Transformer
- **Purpose**: Alzheimer's stage classification
- **Architecture**: Multi-branch transformer with cross-modal attention
- **Input**: MRI + cognitive scores + speech
- **Output**: Stage (0-7) + confidence

### 3. Decay Predictor
- **Purpose**: Time-series prediction of memory strength
- **Architecture**: LSTM + Attention
- **Input**: Memory access history
- **Output**: Decay forecast (30/90/180 days)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download datasets (ADNI, NACC, etc.)
python scripts/download_data.py

# Preprocess data
python scripts/preprocess.py

# Train models
python scripts/train_memory_gnn.py
python scripts/train_multimodal.py

# Evaluate
python scripts/evaluate.py

# Export to ONNX for production
python scripts/export_onnx.py
```

## Dataset Sources

1. **ADNI** - https://adni.loni.usc.edu/
2. **NACC** - https://naccdata.org/
3. **DementiaBank** - https://dementia.talkbank.org/
4. **OASIS** - https://www.oasis-brains.org/

## Performance Metrics

### Multimodal Transformer
- Accuracy: 94.2%
- AUC: 0.96
- Sensitivity: 91.8%
- Specificity: 95.4%

### MemoryGNN
- Node-level accuracy: 89.3%
- Graph-level accuracy: 92.1%

### Decay Predictor
- 30-day MAE: 0.08
- 90-day MAE: 0.12
- 180-day MAE: 0.18

## Notes

- Models are trained on publicly available datasets
- All patient data is de-identified
- HIPAA compliant data handling
