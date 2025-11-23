"""
Memory Graph Neural Network (MemoryGNN)
Predicts memory decay in personal knowledge graph
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool


class MemoryGNN(nn.Module):
    """
    Graph Attention Network for memory decay prediction

    Architecture:
    - Multiple GAT layers with multi-head attention
    - Node-level predictions (memory decay scores)
    - Graph-level aggregation for overall risk assessment
    """

    def __init__(
        self,
        num_node_features: int = 10,
        hidden_channels: int = 64,
        num_heads: int = 4,
        num_layers: int = 3,
        dropout: float = 0.3
    ):
        super(MemoryGNN, self).__init__()

        self.num_layers = num_layers
        self.dropout = dropout

        # Input projection
        self.input_proj = nn.Linear(num_node_features, hidden_channels)

        # GAT layers
        self.gat_layers = nn.ModuleList()
        for i in range(num_layers):
            if i == 0:
                # First layer
                self.gat_layers.append(
                    GATConv(hidden_channels, hidden_channels, heads=num_heads, concat=True)
                )
            elif i == num_layers - 1:
                # Last layer - average heads
                self.gat_layers.append(
                    GATConv(hidden_channels * num_heads, hidden_channels, heads=num_heads, concat=False)
                )
            else:
                # Middle layers
                self.gat_layers.append(
                    GATConv(hidden_channels * num_heads, hidden_channels, heads=num_heads, concat=True)
                )

        # Node-level output (decay prediction per memory)
        self.node_decoder = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels // 2, 3)  # 30-day, 90-day, 180-day predictions
        )

        # Graph-level output (overall risk score)
        self.graph_decoder = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels // 2, 1),
            nn.Sigmoid()  # Risk score 0-1
        )

    def forward(self, x, edge_index, edge_attr=None, batch=None):
        """
        Forward pass

        Args:
            x: Node features [num_nodes, num_features]
            edge_index: Graph connectivity [2, num_edges]
            edge_attr: Edge features (optional)
            batch: Batch assignment for graph-level pooling

        Returns:
            node_predictions: [num_nodes, 3] - Decay predictions
            graph_risk: [batch_size, 1] - Overall risk score
        """
        # Input projection
        x = self.input_proj(x)
        x = F.relu(x)

        # GAT layers
        for i, gat in enumerate(self.gat_layers):
            x = gat(x, edge_index)
            if i < self.num_layers - 1:
                x = F.elu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)

        # Node-level predictions (memory decay)
        node_predictions = self.node_decoder(x)

        # Graph-level prediction (overall risk)
        if batch is None:
            # Single graph
            graph_embedding = torch.mean(x, dim=0, keepdim=True)
        else:
            # Batch of graphs
            graph_embedding = global_mean_pool(x, batch)

        graph_risk = self.graph_decoder(graph_embedding)

        return node_predictions, graph_risk


class MemoryDecayLoss(nn.Module):
    """
    Custom loss function for memory decay prediction
    Combines node-level and graph-level losses
    """

    def __init__(self, alpha=0.7, beta=0.3):
        super(MemoryDecayLoss, self).__init__()
        self.alpha = alpha  # Weight for node-level loss
        self.beta = beta    # Weight for graph-level loss

    def forward(self, node_pred, node_target, graph_pred, graph_target):
        """
        Args:
            node_pred: [num_nodes, 3] - Predicted decay values
            node_target: [num_nodes, 3] - Target decay values
            graph_pred: [batch_size, 1] - Predicted risk scores
            graph_target: [batch_size, 1] - Target risk scores

        Returns:
            loss: Combined loss
        """
        # Node-level loss (MSE for decay prediction)
        node_loss = F.mse_loss(node_pred, node_target)

        # Graph-level loss (BCE for risk classification)
        graph_loss = F.binary_cross_entropy(graph_pred, graph_target)

        # Combined loss
        total_loss = self.alpha * node_loss + self.beta * graph_loss

        return total_loss


# Example usage
if __name__ == "__main__":
    # Create model
    model = MemoryGNN(
        num_node_features=10,
        hidden_channels=64,
        num_heads=4,
        num_layers=3
    )

    # Example data (single graph)
    num_nodes = 20  # 20 memories
    x = torch.randn(num_nodes, 10)  # Node features
    edge_index = torch.randint(0, num_nodes, (2, 40))  # 40 edges

    # Forward pass
    node_pred, graph_risk = model(x, edge_index)

    print(f"Node predictions shape: {node_pred.shape}")  # [20, 3]
    print(f"Graph risk shape: {graph_risk.shape}")  # [1, 1]
    print(f"Graph risk value: {graph_risk.item():.4f}")
