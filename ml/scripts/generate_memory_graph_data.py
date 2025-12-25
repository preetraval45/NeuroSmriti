"""
Generate synthetic memory graph data for GNN training
"""

import torch
import numpy as np
import pickle
import os
from torch_geometric.data import Data
from pathlib import Path


def generate_memory_graph(
    num_memories: int = 50,
    stage: str = "normal",
    patient_age: int = 70
):
    """
    Generate a single patient memory graph

    Args:
        num_memories: Number of memory nodes
        stage: Alzheimer's stage (normal, mci, early, moderate, severe)
        patient_age: Patient age

    Returns:
        PyG Data object
    """
    # Stage-specific parameters
    stage_params = {
        "normal": {"base_decay": 0.05, "connectivity": 0.3, "risk": 0.1},
        "mci": {"base_decay": 0.15, "connectivity": 0.25, "risk": 0.3},
        "early": {"base_decay": 0.30, "connectivity": 0.20, "risk": 0.5},
        "moderate": {"base_decay": 0.50, "connectivity": 0.15, "risk": 0.7},
        "severe": {"base_decay": 0.70, "connectivity": 0.10, "risk": 0.9}
    }

    params = stage_params[stage]

    # Node features (10 features per memory)
    # Features: [memory_type, importance, recency, emotional_valence, rehearsal_count,
    #           contextual_richness, semantic_connections, episodic_detail, age_at_encoding, time_since_encoding]

    node_features = []
    for i in range(num_memories):
        # Memory type (0: episodic, 1: semantic, 2: procedural)
        memory_type = np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])

        # Importance (0-1)
        importance = np.random.beta(2, 2)

        # Recency (0-1, 1 = very recent)
        recency = np.random.exponential(0.3)
        recency = np.clip(recency, 0, 1)

        # Emotional valence (-1 to 1)
        emotional_valence = np.random.normal(0, 0.5)
        emotional_valence = np.clip(emotional_valence, -1, 1)

        # Rehearsal count (normalized 0-1)
        rehearsal_count = np.random.poisson(5) / 20.0
        rehearsal_count = np.clip(rehearsal_count, 0, 1)

        # Contextual richness (0-1)
        contextual_richness = np.random.beta(3, 2)

        # Semantic connections (0-1)
        semantic_connections = np.random.beta(2, 3)

        # Episodic detail (0-1)
        episodic_detail = np.random.beta(3, 2) if memory_type == 0 else np.random.beta(1, 3)

        # Age at encoding (normalized)
        age_at_encoding = (patient_age - np.random.randint(0, min(patient_age, 60))) / 100.0

        # Time since encoding (years, normalized)
        time_since_encoding = np.random.exponential(10) / 50.0
        time_since_encoding = np.clip(time_since_encoding, 0, 1)

        node_features.append([
            memory_type, importance, recency, emotional_valence, rehearsal_count,
            contextual_richness, semantic_connections, episodic_detail,
            age_at_encoding, time_since_encoding
        ])

    x = torch.tensor(node_features, dtype=torch.float)

    # Create edges (memory connections)
    edge_list = []
    edge_weights = []

    for i in range(num_memories):
        # Number of connections decreases with disease stage
        num_connections = int(num_memories * params["connectivity"] * np.random.uniform(0.5, 1.5))
        num_connections = max(1, min(num_connections, num_memories - 1))

        # Connect to random memories (preferring similar memories)
        similarities = np.abs(x[i].numpy() - x.numpy()).sum(axis=1)
        similarities[i] = float('inf')  # Don't connect to self

        # Sample connections based on similarity
        connection_probs = 1 / (similarities + 0.1)
        connection_probs = connection_probs / connection_probs.sum()

        targets = np.random.choice(
            num_memories,
            size=num_connections,
            replace=False,
            p=connection_probs
        )

        for target in targets:
            edge_list.append([i, target])
            # Edge weight based on similarity
            weight = 1.0 / (similarities[target] + 0.1)
            edge_weights.append(weight)

    edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_weights, dtype=torch.float).unsqueeze(1)

    # Target: Memory decay predictions (30, 90, 180 days)
    # Higher decay for less important, older memories and worse disease stage
    y_node = []
    for i in range(num_memories):
        importance = node_features[i][1]
        recency = node_features[i][2]
        rehearsal = node_features[i][4]

        # Base decay rate influenced by stage
        base_decay = params["base_decay"]

        # Protective factors
        protection = (importance * 0.4 + recency * 0.3 + rehearsal * 0.3)

        # Decay at 30, 90, 180 days
        decay_30 = base_decay * (1 - protection * 0.5) + np.random.normal(0, 0.05)
        decay_90 = base_decay * (1 - protection * 0.3) * 1.5 + np.random.normal(0, 0.08)
        decay_180 = base_decay * (1 - protection * 0.2) * 2.0 + np.random.normal(0, 0.10)

        # Clip to 0-1
        decay_30 = np.clip(decay_30, 0, 1)
        decay_90 = np.clip(decay_90, 0, 1)
        decay_180 = np.clip(decay_180, 0, 1)

        y_node.append([decay_30, decay_90, decay_180])

    y_node = torch.tensor(y_node, dtype=torch.float)

    # Graph-level target: Overall memory risk
    y_graph = torch.tensor([[params["risk"]]], dtype=torch.float)

    # Create PyG Data object
    data = Data(
        x=x,
        edge_index=edge_index,
        edge_attr=edge_attr,
        y_node=y_node,
        y_graph=y_graph
    )

    return data


def generate_dataset(
    num_samples: int = 1000,
    stage_distribution: dict = None
):
    """
    Generate a dataset of memory graphs

    Args:
        num_samples: Number of patients
        stage_distribution: Distribution of stages

    Returns:
        List of PyG Data objects
    """
    if stage_distribution is None:
        stage_distribution = {
            "normal": 0.30,
            "mci": 0.25,
            "early": 0.20,
            "moderate": 0.15,
            "severe": 0.10
        }

    stages = list(stage_distribution.keys())
    probs = list(stage_distribution.values())

    dataset = []

    for i in range(num_samples):
        # Random stage
        stage = np.random.choice(stages, p=probs)

        # Random patient age (60-90)
        age = int(np.random.normal(72, 8))
        age = np.clip(age, 60, 90)

        # Random number of memories (varies by stage)
        if stage == "normal":
            num_memories = int(np.random.normal(60, 10))
        elif stage == "mci":
            num_memories = int(np.random.normal(50, 10))
        elif stage == "early":
            num_memories = int(np.random.normal(40, 10))
        elif stage == "moderate":
            num_memories = int(np.random.normal(30, 8))
        else:  # severe
            num_memories = int(np.random.normal(20, 5))

        num_memories = np.clip(num_memories, 15, 100)

        # Generate graph
        data = generate_memory_graph(num_memories, stage, age)
        dataset.append(data)

    return dataset


def main():
    """Generate and save datasets"""
    np.random.seed(42)
    torch.manual_seed(42)

    # Create data directory
    data_dir = Path(__file__).parent.parent / "data" / "synthetic"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Generating memory graph datasets...")

    # Generate datasets
    print("Generating training set (2000 samples)...")
    train_data = generate_dataset(num_samples=2000)

    print("Generating validation set (400 samples)...")
    val_data = generate_dataset(num_samples=400)

    print("Generating test set (400 samples)...")
    test_data = generate_dataset(num_samples=400)

    # Save datasets
    print("\nSaving datasets...")
    with open(data_dir / "train.pkl", "wb") as f:
        pickle.dump(train_data, f)

    with open(data_dir / "val.pkl", "wb") as f:
        pickle.dump(val_data, f)

    with open(data_dir / "test.pkl", "wb") as f:
        pickle.dump(test_data, f)

    # Print statistics
    print("\nDataset Statistics:")
    print(f"Training samples: {len(train_data)}")
    print(f"Validation samples: {len(val_data)}")
    print(f"Test samples: {len(test_data)}")

    # Example graph statistics
    example = train_data[0]
    print(f"\nExample graph:")
    print(f"  Nodes (memories): {example.num_nodes}")
    print(f"  Edges (connections): {example.num_edges}")
    print(f"  Node features: {example.num_node_features}")
    print(f"  Node target shape: {example.y_node.shape}")
    print(f"  Graph risk: {example.y_graph.item():.4f}")

    print("\n✓ Dataset generation complete!")
    print(f"Data saved to: {data_dir}")


if __name__ == "__main__":
    main()
