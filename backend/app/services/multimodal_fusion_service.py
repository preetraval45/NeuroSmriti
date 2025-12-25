"""
Multimodal Fusion Service
Combines MRI/PET imaging data with clinical/cognitive data for enhanced predictions
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional
from pathlib import Path
from loguru import logger
import pickle


class MultimodalFusionModel(nn.Module):
    """
    Multimodal fusion model combining imaging and clinical data

    Architecture:
    - Image branch: Pre-trained 3D CNN (e.g., ResNet3D) for brain scans
    - Clinical branch: Feed-forward network for tabular data
    - Fusion: Concatenation + attention mechanism
    """

    def __init__(
        self,
        num_clinical_features: int = 29,
        num_classes: int = 5,
        image_feature_dim: int = 512,
        clinical_hidden_dim: int = 128,
        fusion_dim: int = 256,
        dropout: float = 0.3
    ):
        super(MultimodalFusionModel, self).__init__()

        # Image branch (2D for now, can be extended to 3D)
        # Using pre-trained ResNet18 as backbone
        resnet = models.resnet18(pretrained=True)

        # Modify first conv layer for grayscale medical images
        resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

        # Remove final classification layer
        self.image_encoder = nn.Sequential(*list(resnet.children())[:-1])

        # Image feature projection
        self.image_proj = nn.Sequential(
            nn.Linear(512, image_feature_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(image_feature_dim, image_feature_dim),
            nn.ReLU()
        )

        # Clinical data branch
        self.clinical_encoder = nn.Sequential(
            nn.Linear(num_clinical_features, clinical_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(clinical_hidden_dim, clinical_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(clinical_hidden_dim, image_feature_dim),  # Match image dim
            nn.ReLU()
        )

        # Attention mechanism for fusion
        self.attention = nn.MultiheadAttention(
            embed_dim=image_feature_dim,
            num_heads=4,
            dropout=dropout
        )

        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(image_feature_dim * 2, fusion_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(fusion_dim, fusion_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Classification head
        self.classifier = nn.Linear(fusion_dim // 2, num_classes)

    def forward(
        self,
        image: Optional[torch.Tensor] = None,
        clinical: Optional[torch.Tensor] = None
    ):
        """
        Forward pass

        Args:
            image: [batch, 1, H, W] - Brain scan image
            clinical: [batch, num_features] - Clinical features

        Returns:
            logits: [batch, num_classes]
        """
        features = []

        # Image branch
        if image is not None:
            img_features = self.image_encoder(image)
            img_features = img_features.view(img_features.size(0), -1)
            img_features = self.image_proj(img_features)
            features.append(img_features)

        # Clinical branch
        if clinical is not None:
            clin_features = self.clinical_encoder(clinical)
            features.append(clin_features)

        # Fusion
        if len(features) == 2:
            # Both modalities available - use attention
            img_feat, clin_feat = features

            # Prepare for attention (sequence_length=1 for each modality)
            img_feat_seq = img_feat.unsqueeze(0)  # [1, batch, dim]
            clin_feat_seq = clin_feat.unsqueeze(0)  # [1, batch, dim]

            # Cross-attention: clinical attends to image
            attn_output, _ = self.attention(
                query=clin_feat_seq,
                key=img_feat_seq,
                value=img_feat_seq
            )

            attn_output = attn_output.squeeze(0)  # [batch, dim]

            # Concatenate attended features with clinical features
            fused = torch.cat([attn_output, clin_feat], dim=1)

        elif len(features) == 1:
            # Single modality - duplicate for fusion layer
            fused = torch.cat([features[0], features[0]], dim=1)
        else:
            raise ValueError("At least one modality (image or clinical) must be provided")

        # Fusion and classification
        fused = self.fusion(fused)
        logits = self.classifier(fused)

        return logits


class MultimodalFusionService:
    """Service for multimodal fusion inference"""

    def __init__(self, model_path: Path = None):
        self.model_path = model_path or Path(__file__).parent.parent / "ml" / "models"
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler = None
        self.label_encoder = None

        # Image preprocessing
        self.image_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])  # Grayscale normalization
        ])

    def load_model(self, model_name: str = "multimodal_fusion_model.pth"):
        """Load trained multimodal fusion model"""
        try:
            model_file = self.model_path / model_name

            if model_file.exists():
                # Load PyTorch model
                checkpoint = torch.load(model_file, map_location=self.device)

                self.model = MultimodalFusionModel(
                    num_clinical_features=checkpoint.get('num_features', 29),
                    num_classes=checkpoint.get('num_classes', 5)
                )

                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.model.to(self.device)
                self.model.eval()

                logger.info(f"Loaded multimodal fusion model from {model_file}")
            else:
                # Initialize new model
                logger.warning(f"Model file {model_file} not found, initializing new model")
                self.model = MultimodalFusionModel()
                self.model.to(self.device)
                self.model.eval()

            # Load scaler and label encoder
            scaler_file = self.model_path / "scaler.pkl"
            if scaler_file.exists():
                with open(scaler_file, "rb") as f:
                    self.scaler = pickle.load(f)

            label_encoder_file = self.model_path / "label_encoder.pkl"
            if label_encoder_file.exists():
                with open(label_encoder_file, "rb") as f:
                    self.label_encoder = pickle.load(f)

        except Exception as e:
            logger.error(f"Error loading multimodal model: {e}")
            raise

    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """
        Preprocess brain scan image

        Args:
            image_path: Path to image file

        Returns:
            Preprocessed image tensor [1, 1, H, W]
        """
        try:
            # Load image
            image = Image.open(image_path).convert('L')  # Convert to grayscale

            # Apply transforms
            image_tensor = self.image_transform(image)

            # Add batch dimension
            image_tensor = image_tensor.unsqueeze(0)  # [1, 1, H, W]

            return image_tensor

        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise

    def predict(
        self,
        clinical_data: Optional[Dict[str, float]] = None,
        image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make prediction using multimodal data

        Args:
            clinical_data: Dictionary of clinical features
            image_path: Path to brain scan image (MRI/PET)

        Returns:
            Prediction results with probabilities
        """
        try:
            if self.model is None:
                self.load_model()

            # Prepare clinical data
            clinical_tensor = None
            if clinical_data is not None and self.scaler is not None:
                # Extract features in correct order
                features = self._extract_features(clinical_data)
                features_scaled = self.scaler.transform([features])
                clinical_tensor = torch.tensor(features_scaled, dtype=torch.float32).to(self.device)

            # Prepare image data
            image_tensor = None
            if image_path is not None:
                image_tensor = self.preprocess_image(image_path).to(self.device)

            # Make prediction
            with torch.no_grad():
                logits = self.model(image=image_tensor, clinical=clinical_tensor)
                probabilities = F.softmax(logits, dim=1)[0].cpu().numpy()

            # Get prediction
            predicted_idx = np.argmax(probabilities)

            if self.label_encoder is not None:
                predicted_stage = self.label_encoder.classes_[predicted_idx]
            else:
                predicted_stage = f"Stage_{predicted_idx}"

            # Calculate confidence
            confidence = float(probabilities[predicted_idx])

            # Prepare results
            results = {
                "prediction": predicted_stage,
                "confidence": confidence,
                "probabilities": {
                    self.label_encoder.classes_[i] if self.label_encoder else f"Stage_{i}": float(prob)
                    for i, prob in enumerate(probabilities)
                },
                "modalities_used": {
                    "clinical_data": clinical_data is not None,
                    "brain_scan": image_path is not None
                },
                "fusion_method": "attention_based"
            }

            return results

        except Exception as e:
            logger.error(f"Error in multimodal prediction: {e}")
            raise

    def _extract_features(self, patient_data: Dict) -> list:
        """Extract features from patient data in correct order"""
        features = [
            patient_data.get('age', 70),
            patient_data.get('gender', 0),
            patient_data.get('education_years', 14),
            patient_data.get('apoe4_positive', 0),
            patient_data.get('mmse_score', 24),
            patient_data.get('moca_score', 22),
            patient_data.get('cdr_score', 0),
            patient_data.get('gds_score', 5),
            patient_data.get('faq_score', 0),
            patient_data.get('adas_cog_score', 10),
            patient_data.get('npi_score', 0),
            patient_data.get('hippocampal_volume', 3200),
            patient_data.get('ventricular_volume', 45000),
            patient_data.get('brain_volume', 1100000),
            patient_data.get('csf_abeta', 650),
            patient_data.get('csf_tau', 350),
            patient_data.get('csf_ptau', 50),
            patient_data.get('fdg_pet', 1.3),
            patient_data.get('pib_pet', 1.4),
            patient_data.get('av45_pet', 1.2),
            patient_data.get('speech_pause_ratio', 0.1),
            patient_data.get('word_finding_difficulty', 2),
            patient_data.get('gait_speed', 1.0),
            patient_data.get('stride_variability', 0.1),
            patient_data.get('sleep_efficiency', 0.85),
            patient_data.get('rem_sleep_percentage', 0.20),
            patient_data.get('physical_activity_minutes', 30),
            patient_data.get('social_engagement_score', 6),
            patient_data.get('cognitive_reserve_score', 100)
        ]
        return features

    def get_attention_weights(
        self,
        clinical_data: Optional[Dict[str, float]] = None,
        image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get attention weights to understand modality importance

        Args:
            clinical_data: Dictionary of clinical features
            image_path: Path to brain scan image

        Returns:
            Attention weights and importance scores
        """
        # This would require modifying the forward pass to return attention weights
        # Placeholder for now
        return {
            "attention_visualization": "Not implemented yet",
            "modality_importance": {
                "imaging": 0.6,
                "clinical": 0.4
            }
        }


# Singleton instance
multimodal_fusion_service = MultimodalFusionService()
