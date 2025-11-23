"""
Generate synthetic memory graph data for training MemoryGNN
This creates realistic memory graphs for Alzheimer's patients at different stages
"""

import torch
import numpy as np
import networkx as nx
from torch_geometric.data import Data
import pickle
import os


def generate_patient_memory_graph(num_memories=20, stage=2, patient_id=0):
    """
    Generate a synthetic memory graph for one patient

    Args:
        num_memories: Number of memory nodes
        stage: Alzheimer's stage (0-7)
        patient_id: Unique patient identifier

    Returns:
        PyTorch Geometric Data object
    """
    # Memory types distribution
    memory_types = {
        'person': 0.35,
        'place': 0.20,
        'event': 0.20,
        'skill': 0.15,
        'routine': 0.10
    }

    # Node features (10 dimensions)
    # [type_one_hot(5), recall_strength(1), emotional_weight(1), importance(1), age_days(1), access_freq(1)]

    node_features = []
    initial_strengths = []

    for i in range(num_memories):
        # One-hot encode memory type
        type_probs = list(memory_types.values())
        mem_type_idx = np.random.choice(len(type_probs), p=type_probs)
        type_onehot = [0.0] * 5
        type_onehot[mem_type_idx] = 1.0

        # Recall strength decreases with Alzheimer's stage
        base_strength = np.random.uniform(60, 100) if stage <= 2 else np.random.uniform(30, 80)
        stage_decay = stage * 8  # Higher stage = more decay
        recall_strength = max(10, base_strength - stage_decay + np.random.normal(0, 10))

        # Emotional memories are stronger
        emotional_weight = np.random.beta(2, 5)  # Skewed toward lower values
        if emotional_weight > 0.8:
            recall_strength += 10  # Boost emotionally significant memories

        # Importance (1-10)
        importance = np.random.randint(3, 11) / 10.0

        # Age of memory (newer = stronger)
        age_days = np.random.exponential(scale=365 * 5) / (365 * 10)  # Normalize to 0-1

        # Access frequency (how often accessed)
        access_freq = np.random.beta(2, 8)  # Most memories rarely accessed

        features = type_onehot + [
            recall_strength / 100.0,  # Normalize
            emotional_weight,
            importance,
            min(age_days, 1.0),
            access_freq
        ]

        node_features.append(features)
        initial_strengths.append(recall_strength)

    x = torch.tensor(node_features, dtype=torch.float)

    # Generate edges (memory connections)
    # More connections for people and events
    edges = []
    edge_weights = []

    for i in range(num_memories):
        # Each node connects to 2-5 other nodes
        num_connections = np.random.randint(2, 6)
        targets = np.random.choice(num_memories, size=num_connections, replace=False)

        for j in targets:
            if i != j:
                edges.append([i, j])

                # Connection strength based on feature similarity
                similarity = 1.0 - np.abs(node_features[i][5] - node_features[j][5])  # Based on recall strength
                edge_weights.append(similarity)

    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_weights, dtype=torch.float).unsqueeze(1)

    # Target: memory decay predictions (30-day, 90-day, 180-day)
    y_node = []
    for i, strength in enumerate(initial_strengths):
        # Decay model: exponential decay faster at higher stages
        decay_rate = 0.01 * (stage + 1) + np.random.normal(0, 0.005)

        decay_30 = max(0, strength - (decay_rate * 30 * strength))
        decay_90 = max(0, strength - (decay_rate * 90 * strength))
        decay_180 = max(0, strength - (decay_rate * 180 * strength))

        # Emotional memories decay slower
        if node_features[i][6] > 0.8:  # High emotional weight
            decay_30 = min(100, decay_30 + 5)
            decay_90 = min(100, decay_90 + 10)
            decay_180 = min(100, decay_180 + 15)

        y_node.append([decay_30 / 100.0, decay_90 / 100.0, decay_180 / 100.0])

    y_node = torch.tensor(y_node, dtype=torch.float)

    # Graph-level target: overall risk score (0-1)
    avg_strength = np.mean(initial_strengths)
    risk_score = 1.0 - (avg_strength / 100.0)
    risk_score = min(1.0, max(0.0, risk_score + stage * 0.05))
    y_graph = torch.tensor([risk_score], dtype=torch.float)

    # Create PyTorch Geometric Data object
    data = Data(
        x=x,
        edge_index=edge_index,
        edge_attr=edge_attr,
        y_node=y_node,
        y_graph=y_graph,
        patient_id=patient_id,
        stage=stage
    )

    return data


def generate_dataset(num_patients=1000, output_dir='../data/synthetic'):
    """
    Generate a complete dataset of memory graphs

    Args:
        num_patients: Number of patients to generate
        output_dir: Where to save the data
    """
    os.makedirs(output_dir, exist_ok=True)

    train_data = []
    val_data = []
    test_data = []

    print(f"Generating {num_patients} synthetic patient memory graphs...")

    for i in range(num_patients):
        # Random stage (0-7), with more patients in stages 1-4
        stage = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7], p=[0.05, 0.15, 0.25, 0.25, 0.15, 0.08, 0.05, 0.02])

        # Random number of memories (10-40)
        num_memories = np.random.randint(10, 41)

        # Generate graph
        data = generate_patient_memory_graph(
            num_memories=num_memories,
            stage=stage,
            patient_id=i
        )

        # Split: 70% train, 15% val, 15% test
        rand = np.random.rand()
        if rand < 0.7:
            train_data.append(data)
        elif rand < 0.85:
            val_data.append(data)
        else:
            test_data.append(data)

        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_patients} patients")

    # Save datasets
    with open(f'{output_dir}/train.pkl', 'wb') as f:
        pickle.dump(train_data, f)

    with open(f'{output_dir}/val.pkl', 'wb') as f:
        pickle.dump(val_data, f)

    with open(f'{output_dir}/test.pkl', 'wb') as f:
        pickle.dump(test_data, f)

    print(f"\nDataset saved to {output_dir}/")
    print(f"Train: {len(train_data)} patients")
    print(f"Val: {len(val_data)} patients")
    print(f"Test: {len(test_data)} patients")

    # Print sample statistics
    all_data = train_data + val_data + test_data
    avg_nodes = np.mean([data.x.size(0) for data in all_data])
    avg_edges = np.mean([data.edge_index.size(1) for data in all_data])

    print(f"\nAverage nodes per graph: {avg_nodes:.1f}")
    print(f"Average edges per graph: {avg_edges:.1f}")


if __name__ == "__main__":
    # Generate dataset
    generate_dataset(num_patients=1000)

    print("\nDone! You can now train the model with:")
    print("python train_memory_gnn.py")
