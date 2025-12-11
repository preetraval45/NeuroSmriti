"""
Clinical Validation Metrics for Alzheimer's Detection

Implements medical-grade evaluation metrics required for clinical AI systems:
- Sensitivity (Recall) - How many actual positive cases are detected
- Specificity - How many actual negative cases are correctly identified
- Precision (PPV) - Of positive predictions, how many are correct
- NPV (Negative Predictive Value)
- F1 Score - Harmonic mean of precision and recall
- AUC-ROC - Area under Receiver Operating Characteristic curve
- AUC-PR - Area under Precision-Recall curve
- Confusion Matrix with confidence intervals
- Multi-class metrics for Alzheimer's stages

Based on FDA guidelines for medical AI systems.
"""

import numpy as np
import torch
from sklearn.metrics import (
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    auc,
    classification_report,
    cohen_kappa_score
)
from scipy.stats import chi2_contingency, bootstrap
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns


class ClinicalMetrics:
    """Calculate clinical validation metrics for Alzheimer's detection"""

    def __init__(self, n_classes=8, class_names=None):
        """
        Args:
            n_classes: Number of Alzheimer's stages (0-7)
            class_names: Names for each class
        """
        self.n_classes = n_classes
        self.class_names = class_names or [f"Stage {i}" for i in range(n_classes)]

    def calculate_all_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Calculate comprehensive clinical metrics

        Args:
            y_true: Ground truth labels (N,)
            y_pred: Predicted labels (N,)
            y_prob: Predicted probabilities (N, n_classes) - optional

        Returns:
            Dictionary with all clinical metrics
        """
        metrics = {}

        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred, labels=range(self.n_classes))
        metrics['confusion_matrix'] = cm

        # Per-class metrics
        metrics['per_class'] = self._calculate_per_class_metrics(y_true, y_pred)

        # Overall metrics
        metrics['overall'] = self._calculate_overall_metrics(y_true, y_pred)

        # Clinical significance metrics
        metrics['clinical'] = self._calculate_clinical_metrics(y_true, y_pred)

        # If probabilities provided, calculate AUC metrics
        if y_prob is not None:
            metrics['auc'] = self._calculate_auc_metrics(y_true, y_prob)

        # Cohen's Kappa (inter-rater agreement)
        metrics['cohens_kappa'] = cohen_kappa_score(y_true, y_pred)

        return metrics

    def _calculate_per_class_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict:
        """Calculate sensitivity, specificity, PPV, NPV for each class"""

        per_class_metrics = {}

        for class_idx in range(self.n_classes):
            # Binary classification: this class vs all others
            y_true_binary = (y_true == class_idx).astype(int)
            y_pred_binary = (y_pred == class_idx).astype(int)

            # Calculate confusion matrix for this class
            tn, fp, fn, tp = self._binary_confusion_matrix(y_true_binary, y_pred_binary)

            # Sensitivity (Recall, True Positive Rate)
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0

            # Specificity (True Negative Rate)
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

            # Precision (Positive Predictive Value)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

            # Negative Predictive Value
            npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0

            # F1 Score
            f1 = 2 * (precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0.0

            # Accuracy for this class
            accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0

            # Calculate 95% confidence intervals using Wilson score
            ci_sensitivity = self._wilson_score_interval(tp, tp + fn)
            ci_specificity = self._wilson_score_interval(tn, tn + fp)
            ci_precision = self._wilson_score_interval(tp, tp + fp)

            per_class_metrics[self.class_names[class_idx]] = {
                'sensitivity': sensitivity,
                'specificity': specificity,
                'precision': precision,
                'npv': npv,
                'f1_score': f1,
                'accuracy': accuracy,
                'support': int(np.sum(y_true == class_idx)),
                'ci_95': {
                    'sensitivity': ci_sensitivity,
                    'specificity': ci_specificity,
                    'precision': ci_precision
                }
            }

        return per_class_metrics

    def _calculate_overall_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict:
        """Calculate overall performance metrics"""

        # Overall accuracy
        accuracy = np.mean(y_true == y_pred)

        # Macro-averaged metrics (average across classes)
        per_class = self._calculate_per_class_metrics(y_true, y_pred)

        macro_sensitivity = np.mean([m['sensitivity'] for m in per_class.values()])
        macro_specificity = np.mean([m['specificity'] for m in per_class.values()])
        macro_precision = np.mean([m['precision'] for m in per_class.values()])
        macro_f1 = np.mean([m['f1_score'] for m in per_class.values()])

        # Weighted metrics (weighted by class support)
        total_support = len(y_true)
        weighted_sensitivity = sum(
            m['sensitivity'] * m['support'] for m in per_class.values()
        ) / total_support
        weighted_specificity = sum(
            m['specificity'] * m['support'] for m in per_class.values()
        ) / total_support
        weighted_f1 = sum(
            m['f1_score'] * m['support'] for m in per_class.values()
        ) / total_support

        return {
            'accuracy': accuracy,
            'macro_avg': {
                'sensitivity': macro_sensitivity,
                'specificity': macro_specificity,
                'precision': macro_precision,
                'f1_score': macro_f1
            },
            'weighted_avg': {
                'sensitivity': weighted_sensitivity,
                'specificity': weighted_specificity,
                'f1_score': weighted_f1
            }
        }

    def _calculate_clinical_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict:
        """Calculate clinically relevant metrics"""

        # Adjacent accuracy (predictions within 1 stage)
        adjacent_correct = np.abs(y_true - y_pred) <= 1
        adjacent_accuracy = np.mean(adjacent_correct)

        # Early detection accuracy (stages 0-2)
        early_stage_mask = y_true <= 2
        early_stage_accuracy = np.mean(
            y_true[early_stage_mask] == y_pred[early_stage_mask]
        ) if np.any(early_stage_mask) else 0.0

        # Late detection accuracy (stages 5-7)
        late_stage_mask = y_true >= 5
        late_stage_accuracy = np.mean(
            y_true[late_stage_mask] == y_pred[late_stage_mask]
        ) if np.any(late_stage_mask) else 0.0

        # Severity overestimation/underestimation
        overestimation_rate = np.mean(y_pred > y_true)
        underestimation_rate = np.mean(y_pred < y_true)

        # Mean absolute error
        mae = np.mean(np.abs(y_true - y_pred))

        return {
            'adjacent_accuracy': adjacent_accuracy,
            'early_stage_accuracy': early_stage_accuracy,
            'late_stage_accuracy': late_stage_accuracy,
            'overestimation_rate': overestimation_rate,
            'underestimation_rate': underestimation_rate,
            'mean_absolute_error': mae
        }

    def _calculate_auc_metrics(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray
    ) -> Dict:
        """Calculate AUC-ROC and AUC-PR for multi-class"""

        auc_metrics = {}

        # One-vs-Rest AUC for each class
        for class_idx in range(self.n_classes):
            y_true_binary = (y_true == class_idx).astype(int)
            y_score = y_prob[:, class_idx]

            # Skip if class not present
            if len(np.unique(y_true_binary)) < 2:
                continue

            # AUC-ROC
            auc_roc = roc_auc_score(y_true_binary, y_score)

            # AUC-PR
            precision, recall, _ = precision_recall_curve(y_true_binary, y_score)
            auc_pr = auc(recall, precision)

            auc_metrics[self.class_names[class_idx]] = {
                'auc_roc': auc_roc,
                'auc_pr': auc_pr
            }

        # Macro-average AUC
        if auc_metrics:
            auc_metrics['macro_avg'] = {
                'auc_roc': np.mean([m['auc_roc'] for m in auc_metrics.values() if isinstance(m, dict)]),
                'auc_pr': np.mean([m['auc_pr'] for m in auc_metrics.values() if isinstance(m, dict)])
            }

        return auc_metrics

    @staticmethod
    def _binary_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[int, int, int, int]:
        """Calculate TN, FP, FN, TP for binary classification"""
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        tn, fp = cm[0]
        fn, tp = cm[1]
        return tn, fp, fn, tp

    @staticmethod
    def _wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float]:
        """
        Calculate Wilson score confidence interval for binomial proportion

        More accurate than normal approximation for small sample sizes
        """
        if trials == 0:
            return (0.0, 0.0)

        from scipy.stats import norm
        z = norm.ppf(1 - (1 - confidence) / 2)

        p = successes / trials
        denominator = 1 + z**2 / trials

        center = (p + z**2 / (2 * trials)) / denominator
        margin = z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator

        return (max(0, center - margin), min(1, center + margin))

    def print_report(self, metrics: Dict):
        """Print comprehensive clinical validation report"""

        print("\n" + "="*80)
        print("CLINICAL VALIDATION METRICS REPORT")
        print("="*80)

        # Overall metrics
        print("\n📊 OVERALL PERFORMANCE")
        print("-" * 80)
        overall = metrics['overall']
        print(f"Accuracy:                    {overall['accuracy']:.4f}")
        print(f"Cohen's Kappa:               {metrics['cohens_kappa']:.4f}")

        print("\nMacro-Averaged Metrics (Equal weight to each class):")
        macro = overall['macro_avg']
        print(f"  Sensitivity (Recall):      {macro['sensitivity']:.4f}")
        print(f"  Specificity:               {macro['specificity']:.4f}")
        print(f"  Precision:                 {macro['precision']:.4f}")
        print(f"  F1 Score:                  {macro['f1_score']:.4f}")

        print("\nWeighted Metrics (Weighted by class frequency):")
        weighted = overall['weighted_avg']
        print(f"  Sensitivity:               {weighted['sensitivity']:.4f}")
        print(f"  Specificity:               {weighted['specificity']:.4f}")
        print(f"  F1 Score:                  {weighted['f1_score']:.4f}")

        # Clinical metrics
        print("\n🏥 CLINICAL SIGNIFICANCE")
        print("-" * 80)
        clinical = metrics['clinical']
        print(f"Adjacent Accuracy (±1 stage):     {clinical['adjacent_accuracy']:.4f}")
        print(f"Early Stage Detection (0-2):      {clinical['early_stage_accuracy']:.4f}")
        print(f"Late Stage Detection (5-7):       {clinical['late_stage_accuracy']:.4f}")
        print(f"Mean Absolute Error:              {clinical['mean_absolute_error']:.4f}")
        print(f"Overestimation Rate:              {clinical['overestimation_rate']:.4f}")
        print(f"Underestimation Rate:             {clinical['underestimation_rate']:.4f}")

        # Per-class metrics
        print("\n📋 PER-CLASS PERFORMANCE")
        print("-" * 80)
        print(f"{'Class':<20} {'Sens':<8} {'Spec':<8} {'Prec':<8} {'F1':<8} {'Support':<8}")
        print("-" * 80)

        for class_name, class_metrics in metrics['per_class'].items():
            print(f"{class_name:<20} "
                  f"{class_metrics['sensitivity']:<8.4f} "
                  f"{class_metrics['specificity']:<8.4f} "
                  f"{class_metrics['precision']:<8.4f} "
                  f"{class_metrics['f1_score']:<8.4f} "
                  f"{class_metrics['support']:<8}")

        # AUC metrics if available
        if 'auc' in metrics and metrics['auc']:
            print("\n📈 AUC METRICS")
            print("-" * 80)
            print(f"{'Class':<20} {'AUC-ROC':<10} {'AUC-PR':<10}")
            print("-" * 80)

            for class_name, auc_vals in metrics['auc'].items():
                if isinstance(auc_vals, dict):
                    print(f"{class_name:<20} "
                          f"{auc_vals['auc_roc']:<10.4f} "
                          f"{auc_vals['auc_pr']:<10.4f}")

        print("\n" + "="*80)

    def plot_confusion_matrix(self, cm: np.ndarray, save_path: Optional[str] = None):
        """Plot confusion matrix heatmap"""

        plt.figure(figsize=(12, 10))

        # Normalize confusion matrix
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        sns.heatmap(
            cm_normalized,
            annot=True,
            fmt='.2f',
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            cbar_kws={'label': 'Proportion'}
        )

        plt.title('Confusion Matrix (Normalized)', fontsize=16, fontweight='bold')
        plt.ylabel('True Stage', fontsize=12)
        plt.xlabel('Predicted Stage', fontsize=12)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Confusion matrix saved to: {save_path}")
        else:
            plt.show()

        plt.close()


def main():
    """Demo usage of clinical metrics"""

    # Simulate predictions
    np.random.seed(42)
    n_samples = 1000

    y_true = np.random.randint(0, 8, n_samples)
    y_pred = np.clip(y_true + np.random.randint(-1, 2, n_samples), 0, 7)
    y_prob = np.random.dirichlet(np.ones(8), n_samples)

    # Calculate metrics
    evaluator = ClinicalMetrics(n_classes=8)
    metrics = evaluator.calculate_all_metrics(y_true, y_pred, y_prob)

    # Print report
    evaluator.print_report(metrics)

    # Plot confusion matrix
    evaluator.plot_confusion_matrix(metrics['confusion_matrix'])


if __name__ == "__main__":
    main()
