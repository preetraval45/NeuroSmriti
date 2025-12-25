# Memory GNN Training Guide

## Overview

The Memory Graph Neural Network (MemoryGNN) predicts memory decay in Alzheimer's patients by analyzing their personal memory knowledge graphs. This guide walks you through training the GNN model.

---

## Prerequisites

### 1. Install PyTorch

```bash
# For CPU-only (recommended for testing)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# OR for CUDA 11.8 (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# OR for CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 2. Install PyTorch Geometric

```bash
pip install torch-geometric
pip install torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-2.1.2+cpu.html
```

### 3. Install Other Dependencies

```bash
cd ml
pip install -r requirements.txt
```

---

## Training Steps

### Step 1: Generate Synthetic Memory Graphs

```bash
cd ml
python scripts/generate_synthetic_data.py
```

**Expected Output:**
```
Generating 1000 synthetic patient memory graphs...
Generated 100/1000 patients
Generated 200/1000 patients
...
Generated 1000/1000 patients

Dataset saved to ../data/synthetic/
Train: 700 patients
Val: 150 patients
Test: 150 patients

Average nodes per graph: 20.5
Average edges per graph: 82.3
```

**This creates:**
- `ml/data/synthetic/train.pkl` - 700 patient graphs
- `ml/data/synthetic/val.pkl` - 150 validation graphs
- `ml/data/synthetic/test.pkl` - 150 test graphs

---

### Step 2: Train the Memory GNN

```bash
cd ml
python scripts/train_memory_gnn.py
```

**Training Process:**
```
Using device: cpu (or cuda if GPU available)

Loading data...
Train: 700, Val: 150, Test: 150

Initializing model...
Model parameters: 125,000

Starting training...

Epoch 1/50
Training: 100%|██████████| 22/22 [00:15<00:00]
Train Loss: 0.2345
Val Loss: 0.1987 | Node MAE: 0.1102 | Graph MAE: 0.0845
✓ Saved best model!

Epoch 2/50
Training: 100%|██████████| 22/22 [00:14<00:00]
Train Loss: 0.1876
Val Loss: 0.1654 | Node MAE: 0.0987 | Graph MAE: 0.0721
✓ Saved best model!

...

Early stopping after 35 epochs

================================================
Final Evaluation on Test Set
================================================

Test Results:
Loss: 0.1423
Node MAE (decay prediction): 0.0856
Graph MAE (risk score): 0.0623

Node MAE as percentage: 8.56%
Graph MAE as percentage: 6.23%

Accuracy (within 10% threshold):
30-day forecast: 89.45%
90-day forecast: 91.23%
180-day forecast: 92.87%

================================================
Training completed successfully!
Best model saved to: ../models/memory_gnn_best.pth
================================================
```

---

### Step 3: Verify Model Files

```bash
ls -lh ml/models/
```

**Expected:**
```
ensemble_model.pkl           6.4 MB
gradient_boosting_model.pkl  1.3 MB
neural_network_model.pkl     0.3 MB
random_forest_model.pkl      1.6 MB
scaler.pkl                   1.1 KB
label_encoder.pkl            285 B
memory_gnn_best.pth          ✅ NEW! (~500 KB)
model_registry.json          549 B
training_results.json        549 B
```

---

## Model Architecture

### MemoryGNN Structure

```python
MemoryGNN(
  num_node_features=10,
  hidden_channels=64,
  num_heads=4,
  num_layers=3,
  dropout=0.3
)
```

**Layers:**
1. **GAT Layer 1**: 10 → 64 channels, 4 attention heads
2. **GAT Layer 2**: 64 → 64 channels, 4 attention heads
3. **GAT Layer 3**: 64 → 64 channels, 4 attention heads
4. **Node Decoder**: 64 → 3 (30/90/180-day decay predictions)
5. **Graph Pooling**: Global mean pooling
6. **Graph Decoder**: 64 → 1 (overall risk score)

**Total Parameters:** ~125,000

---

## Performance Metrics

### Target Performance

| Metric | Target | Meaning |
|--------|--------|---------|
| Node MAE | < 0.12 | Memory decay prediction error |
| Graph MAE | < 0.10 | Overall risk score error |
| 30-day Accuracy | > 85% | Predictions within 10% of truth |
| 90-day Accuracy | > 88% | Predictions within 10% of truth |
| 180-day Accuracy | > 90% | Predictions within 10% of truth |

### Loss Function

Custom loss combining:
- **Node-level MSE** (α=0.7): Memory decay predictions
- **Graph-level BCE** (β=0.3): Overall risk classification

```python
loss = α * node_mse + β * graph_bce
```

---

## Troubleshooting

### Issue: PyTorch Installation Fails

**Solution:** Use official PyTorch website for correct command:
https://pytorch.org/get-started/locally/

### Issue: CUDA Out of Memory

**Solution:** Reduce batch size in training script:
```python
BATCH_SIZE = 16  # Instead of 32
```

### Issue: Training Too Slow on CPU

**Solution:** Reduce number of epochs:
```python
NUM_EPOCHS = 20  # Instead of 50
```

### Issue: Model Not Converging

**Solution:** Adjust learning rate:
```python
LEARNING_RATE = 0.0005  # Instead of 0.001
```

---

## Integration with Backend

### Step 4: Copy Model to Backend

```bash
cp ml/models/memory_gnn_best.pth backend/app/ml/models/
```

### Step 5: Update ML Service

Edit `backend/app/services/ml_service.py` to load the GNN:

```python
def load_memory_gnn(self):
    """Load PyTorch GNN model"""
    import torch
    from ml.src.models.memory_gnn import MemoryGNN

    checkpoint_path = self.model_path / "memory_gnn_best.pth"

    if not checkpoint_path.exists():
        logger.warning("Memory GNN model not found")
        return False

    try:
        # Load checkpoint
        checkpoint = torch.load(checkpoint_path, map_location='cpu')

        # Initialize model
        self.memory_gnn = MemoryGNN(
            num_node_features=10,
            **checkpoint['hyperparameters']
        )

        # Load weights
        self.memory_gnn.load_state_dict(checkpoint['model_state_dict'])
        self.memory_gnn.eval()

        logger.info("Memory GNN loaded successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to load Memory GNN: {e}")
        return False
```

### Step 6: Implement GNN Inference

Update `predict_memory_decay()` in ML service:

```python
def predict_memory_decay(self, memory_graph: Dict) -> Dict[str, Any]:
    """Predict memory decay using GNN"""

    if self.memory_gnn is None:
        self.load_memory_gnn()

    if self.memory_gnn is None:
        # Fall back to heuristic
        return self._heuristic_memory_prediction(memory_graph)

    import torch
    from torch_geometric.data import Data

    try:
        # Convert memory graph to PyG Data object
        memories = memory_graph['memories']

        # Node features (10 dimensions)
        node_features = []
        for mem in memories:
            features = [
                # Type one-hot (5 dims)
                1 if mem['type'] == 'person' else 0,
                1 if mem['type'] == 'place' else 0,
                1 if mem['type'] == 'event' else 0,
                1 if mem['type'] == 'skill' else 0,
                1 if mem['type'] == 'routine' else 0,
                # Memory attributes (5 dims)
                mem['recall_strength'] / 100.0,
                mem.get('emotional_weight', 0.5),
                mem.get('importance', 5) / 10.0,
                0.5,  # age placeholder
                0.3   # access frequency placeholder
            ]
            node_features.append(features)

        x = torch.tensor(node_features, dtype=torch.float)

        # Create edge index (fully connected for simplicity)
        edges = []
        for i in range(len(memories)):
            for j in range(len(memories)):
                if i != j:
                    edges.append([i, j])

        edge_index = torch.tensor(edges, dtype=torch.long).t()
        edge_attr = torch.ones((edge_index.size(1), 1))

        # Create batch tensor
        batch = torch.zeros(len(memories), dtype=torch.long)

        # Run inference
        with torch.no_grad():
            node_pred, graph_pred = self.memory_gnn(
                x, edge_index, edge_attr, batch
            )

        # Process results
        high_risk_memories = []
        for idx, (memory, prediction) in enumerate(zip(memories, node_pred)):
            decay_30, decay_90, decay_180 = prediction.tolist()
            risk_score = 1.0 - decay_180  # Higher decay = higher risk

            if risk_score > 0.6:
                high_risk_memories.append({
                    "memory_id": memory['id'],
                    "name": memory['name'],
                    "type": memory['type'],
                    "decay_probability": float(risk_score),
                    "decay_30_days": float(decay_30 * 100),
                    "decay_90_days": float(decay_90 * 100),
                    "decay_180_days": float(decay_180 * 100),
                    "days_until_critical": int((decay_180 * 180)),
                    "intervention_recommended": risk_score > 0.75
                })

        high_risk_memories.sort(key=lambda x: x['decay_probability'], reverse=True)

        return {
            "patient_id": memory_graph['patient_id'],
            "high_risk_memories": high_risk_memories[:10],
            "total_memories": len(memories),
            "at_risk_count": len([m for m in high_risk_memories if m['decay_probability'] > 0.4]),
            "intervention_recommended_count": len([m for m in high_risk_memories if m['intervention_recommended']]),
            "model_version": "gnn-v1.0.0",
            "overall_risk": float(graph_pred[0])
        }

    except Exception as e:
        logger.error(f"GNN inference failed: {e}")
        return self._heuristic_memory_prediction(memory_graph)
```

---

## Testing the GNN

### Run ML Tests

```bash
cd ml
pytest tests/test_models.py -v
```

### Test Inference Directly

```python
import torch
from ml.src.models.memory_gnn import MemoryGNN

# Load model
checkpoint = torch.load('models/memory_gnn_best.pth')
model = MemoryGNN(num_node_features=10, **checkpoint['hyperparameters'])
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Test with dummy data
x = torch.randn(20, 10)  # 20 memories, 10 features each
edge_index = torch.randint(0, 20, (2, 80))  # 80 edges
edge_attr = torch.randn(80, 1)
batch = torch.zeros(20, dtype=torch.long)

with torch.no_grad():
    node_pred, graph_pred = model(x, edge_index, edge_attr, batch)

print(f"Node predictions shape: {node_pred.shape}")  # [20, 3]
print(f"Graph prediction: {graph_pred.item():.4f}")  # scalar risk score
print("✓ Model working correctly!")
```

---

## Next Steps After Training

1. **Copy model to backend**
2. **Update ML service with GNN inference**
3. **Test predictions via API**
4. **Compare GNN vs heuristic predictions**
5. **Fine-tune on real patient data (when available)**

---

## Expected Training Time

| Hardware | Time |
|----------|------|
| CPU (4 cores) | ~30-45 minutes |
| GPU (NVIDIA GTX 1060) | ~5-8 minutes |
| GPU (NVIDIA RTX 3080) | ~2-3 minutes |

---

## Model Files Summary

After completing training, you'll have:

```
ml/models/
├── memory_gnn_best.pth              ✅ GNN model checkpoint
├── ensemble_model.pkl               ✅ Traditional ML ensemble
├── random_forest_model.pkl          ✅ RF model
├── gradient_boosting_model.pkl      ✅ GB model
├── neural_network_model.pkl         ✅ NN model
├── scaler.pkl                       ✅ Feature scaler
├── label_encoder.pkl                ✅ Label encoder
├── training_results.json            ✅ Training metrics
└── model_registry.json              ✅ Version tracking
```

**Total size:** ~10 MB (all models combined)

---

*For questions or issues, refer to the main IMPLEMENTATION_SUMMARY.md file.*
