"""
Comprehensive Alzheimer's Disease Training Dataset Generator

This module creates a large synthetic dataset for training AI models to detect
and predict Alzheimer's disease progression. The data is based on clinical research
from multiple sources including:

- ADNI (Alzheimer's Disease Neuroimaging Initiative)
- OASIS (Open Access Series of Imaging Studies)
- NACC (National Alzheimer's Coordinating Center)
- Clinical research papers and meta-analyses

The dataset includes:
1. Demographic data
2. Cognitive assessment scores (MMSE, MoCA, CDR)
3. Neuroimaging biomarkers
4. Genetic risk factors (APOE)
5. Lifestyle factors
6. Medical history
7. Speech and language markers
8. Daily activity patterns
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import math

# =====================================================
# CLINICAL REFERENCE DATA FROM RESEARCH
# =====================================================

# CDR (Clinical Dementia Rating) Stages
CDR_STAGES = {
    0: "Normal",
    0.5: "Very Mild Dementia (MCI)",
    1: "Mild Dementia",
    2: "Moderate Dementia",
    3: "Severe Dementia"
}

# MMSE Score Ranges by Stage (Mini-Mental State Examination)
MMSE_RANGES = {
    "normal": (27, 30),
    "mci": (24, 27),
    "mild": (20, 24),
    "moderate": (10, 20),
    "severe": (0, 10)
}

# MoCA Score Ranges (Montreal Cognitive Assessment)
MOCA_RANGES = {
    "normal": (26, 30),
    "mci": (22, 26),
    "mild": (17, 22),
    "moderate": (10, 17),
    "severe": (0, 10)
}

# APOE Genotypes and Risk Factors
APOE_GENOTYPES = {
    "e2/e2": {"frequency": 0.01, "risk_multiplier": 0.6},
    "e2/e3": {"frequency": 0.11, "risk_multiplier": 0.6},
    "e2/e4": {"frequency": 0.02, "risk_multiplier": 2.6},
    "e3/e3": {"frequency": 0.60, "risk_multiplier": 1.0},
    "e3/e4": {"frequency": 0.21, "risk_multiplier": 3.2},
    "e4/e4": {"frequency": 0.05, "risk_multiplier": 14.9}
}

# Brain Region Volumes (normalized, as percentage of intracranial volume)
BRAIN_REGIONS = {
    "hippocampus": {"normal": (0.52, 0.58), "mci": (0.45, 0.52), "ad": (0.35, 0.45)},
    "entorhinal_cortex": {"normal": (0.18, 0.22), "mci": (0.14, 0.18), "ad": (0.08, 0.14)},
    "temporal_lobe": {"normal": (8.0, 9.0), "mci": (7.2, 8.0), "ad": (6.0, 7.2)},
    "parietal_lobe": {"normal": (7.5, 8.5), "mci": (6.8, 7.5), "ad": (5.8, 6.8)},
    "frontal_lobe": {"normal": (12.0, 13.5), "mci": (11.0, 12.0), "ad": (9.5, 11.0)},
    "whole_brain": {"normal": (75, 82), "mci": (70, 75), "ad": (60, 70)}
}

# CSF Biomarkers (pg/mL)
CSF_BIOMARKERS = {
    "abeta42": {"normal": (500, 1200), "mci": (350, 500), "ad": (150, 350)},
    "tau": {"normal": (100, 300), "mci": (300, 500), "ad": (500, 1200)},
    "ptau181": {"normal": (15, 40), "mci": (40, 70), "ad": (70, 150)}
}

# Speech and Language Markers
SPEECH_MARKERS = {
    "words_per_minute": {"normal": (120, 150), "mci": (90, 120), "ad": (50, 90)},
    "pause_frequency": {"normal": (2, 5), "mci": (5, 10), "ad": (10, 20)},
    "word_finding_difficulties": {"normal": (0, 2), "mci": (2, 5), "ad": (5, 15)},
    "semantic_errors": {"normal": (0, 1), "mci": (1, 3), "ad": (3, 10)},
    "repetitions": {"normal": (0, 2), "mci": (2, 5), "ad": (5, 15)}
}

# Daily Activity Patterns
ACTIVITY_MARKERS = {
    "sleep_hours": {"normal": (6.5, 8.5), "mci": (5, 7), "ad": (4, 10)},
    "sleep_disruptions": {"normal": (0, 2), "mci": (2, 5), "ad": (5, 10)},
    "phone_usage_minutes": {"normal": (30, 120), "mci": (15, 45), "ad": (0, 20)},
    "social_interactions": {"normal": (3, 10), "mci": (1, 4), "ad": (0, 2)},
    "medication_adherence": {"normal": (0.9, 1.0), "mci": (0.7, 0.9), "ad": (0.3, 0.7)},
    "wandering_incidents": {"normal": (0, 0), "mci": (0, 1), "ad": (1, 5)}
}

# Risk Factor Weights
RISK_FACTORS = {
    "age": {"weight": 0.25, "threshold": 65},
    "family_history": {"weight": 0.15},
    "apoe4": {"weight": 0.20},
    "education_years": {"weight": -0.10, "threshold": 12},
    "cardiovascular": {"weight": 0.12},
    "diabetes": {"weight": 0.08},
    "depression": {"weight": 0.05},
    "head_injury": {"weight": 0.05},
    "smoking": {"weight": 0.05},
    "physical_inactivity": {"weight": 0.08},
    "social_isolation": {"weight": 0.07}
}

# Medications commonly used
MEDICATIONS = {
    "cholinesterase_inhibitors": ["Donepezil", "Rivastigmine", "Galantamine"],
    "nmda_antagonists": ["Memantine"],
    "combination": ["Namzaric"],
    "supportive": ["Antidepressants", "Antipsychotics", "Anxiolytics", "Sleep aids"]
}

# Ethnicities with different risk profiles
ETHNICITIES = {
    "Caucasian": {"frequency": 0.60, "risk_modifier": 1.0},
    "African American": {"frequency": 0.13, "risk_modifier": 1.5},
    "Hispanic": {"frequency": 0.18, "risk_modifier": 1.3},
    "Asian": {"frequency": 0.06, "risk_modifier": 0.8},
    "Other": {"frequency": 0.03, "risk_modifier": 1.0}
}


class AlzheimersDatasetGenerator:
    """Generate comprehensive Alzheimer's disease dataset for AI training."""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.patient_id_counter = 0

    def _weighted_choice(self, options: Dict[str, Dict]) -> str:
        """Select from options based on frequency weights."""
        items = list(options.keys())
        weights = [options[k]["frequency"] for k in items]
        return random.choices(items, weights=weights)[0]

    def _get_value_in_range(self, range_tuple: tuple, noise: float = 0.1) -> float:
        """Get a value within a range with optional noise."""
        min_val, max_val = range_tuple
        base = random.uniform(min_val, max_val)
        noise_val = random.gauss(0, (max_val - min_val) * noise)
        return max(min_val, min(max_val, base + noise_val))

    def generate_demographics(self, stage: str) -> Dict[str, Any]:
        """Generate demographic data for a patient."""
        # Age distribution varies by stage
        age_ranges = {
            "normal": (55, 75),
            "mci": (60, 80),
            "mild": (65, 85),
            "moderate": (70, 90),
            "severe": (75, 95)
        }

        age = int(self._get_value_in_range(age_ranges[stage]))

        # Gender (slightly higher female prevalence in AD)
        gender_weights = {"normal": 0.5, "mci": 0.52, "mild": 0.55, "moderate": 0.58, "severe": 0.60}
        is_female = random.random() < gender_weights[stage]

        ethnicity = self._weighted_choice(ETHNICITIES)

        # Education years (higher education is protective)
        education_base = {"normal": 14, "mci": 13, "mild": 12, "moderate": 11, "severe": 10}
        education = max(0, int(random.gauss(education_base[stage], 3)))

        return {
            "age": age,
            "gender": "Female" if is_female else "Male",
            "ethnicity": ethnicity,
            "education_years": education,
            "marital_status": random.choice(["Married", "Single", "Widowed", "Divorced"]),
            "living_situation": random.choice(["Independent", "With family", "Assisted living", "Nursing home"]) if stage in ["moderate", "severe"] else random.choice(["Independent", "With family"])
        }

    def generate_genetic_data(self, stage: str) -> Dict[str, Any]:
        """Generate genetic risk factor data."""
        apoe = self._weighted_choice(APOE_GENOTYPES)

        # Family history correlates with stage
        family_history_prob = {"normal": 0.15, "mci": 0.25, "mild": 0.35, "moderate": 0.40, "severe": 0.45}
        has_family_history = random.random() < family_history_prob[stage]

        return {
            "apoe_genotype": apoe,
            "apoe_risk_multiplier": APOE_GENOTYPES[apoe]["risk_multiplier"],
            "has_apoe4_allele": "e4" in apoe,
            "family_history_alzheimers": has_family_history,
            "family_history_dementia": has_family_history or random.random() < 0.2,
            "other_genetic_markers": {
                "TREM2": random.random() < 0.02,
                "SORL1": random.random() < 0.03,
                "CLU": random.random() < 0.10,
                "PICALM": random.random() < 0.08
            }
        }

    def generate_cognitive_scores(self, stage: str) -> Dict[str, Any]:
        """Generate cognitive assessment scores."""
        mmse = self._get_value_in_range(MMSE_RANGES[stage])
        moca = self._get_value_in_range(MOCA_RANGES[stage])

        # CDR mapping
        cdr_map = {"normal": 0, "mci": 0.5, "mild": 1, "moderate": 2, "severe": 3}
        cdr = cdr_map[stage]

        # Generate subscores
        return {
            "mmse_total": round(mmse, 1),
            "mmse_orientation": round(self._get_value_in_range((max(0, mmse/3-1), min(10, mmse/3+1))), 1),
            "mmse_registration": round(min(3, max(0, mmse/10)), 1),
            "mmse_attention": round(self._get_value_in_range((max(0, mmse/6-1), min(5, mmse/6+1))), 1),
            "mmse_recall": round(min(3, max(0, (mmse-20)/3.3)), 1),
            "mmse_language": round(self._get_value_in_range((max(0, mmse/3.3-1), min(9, mmse/3.3+1))), 1),
            "moca_total": round(moca, 1),
            "moca_visuospatial": round(self._get_value_in_range((max(0, moca/6-0.5), min(5, moca/6+0.5))), 1),
            "moca_naming": round(min(3, max(0, moca/10)), 1),
            "moca_attention": round(self._get_value_in_range((max(0, moca/5-1), min(6, moca/5+1))), 1),
            "moca_language": round(self._get_value_in_range((max(0, moca/10-0.5), min(3, moca/10+0.5))), 1),
            "moca_abstraction": round(min(2, max(0, moca/15)), 1),
            "moca_delayed_recall": round(min(5, max(0, (moca-15)/3)), 1),
            "moca_orientation": round(min(6, max(0, moca/5)), 1),
            "cdr_global": cdr,
            "cdr_memory": cdr + random.choice([-0.5, 0, 0.5]) if cdr > 0 else 0,
            "cdr_orientation": cdr,
            "cdr_judgment": cdr + random.choice([-0.5, 0, 0]) if cdr > 0 else 0,
            "cdr_community": cdr,
            "cdr_home_hobbies": cdr + random.choice([0, 0.5]) if cdr > 0 else 0,
            "cdr_personal_care": max(0, cdr - 0.5) if cdr < 3 else 3,
            "diagnosis_stage": stage,
            "diagnosis_label": CDR_STAGES[cdr]
        }

    def generate_neuroimaging(self, stage: str) -> Dict[str, Any]:
        """Generate neuroimaging biomarker data."""
        stage_key = "ad" if stage in ["mild", "moderate", "severe"] else stage
        if stage_key == "normal":
            stage_key = "normal"
        elif stage_key == "mci":
            stage_key = "mci"
        else:
            stage_key = "ad"

        brain_volumes = {}
        for region, ranges in BRAIN_REGIONS.items():
            brain_volumes[f"{region}_volume"] = round(self._get_value_in_range(ranges[stage_key]), 3)

        # Atrophy rates (% per year)
        atrophy_rates = {
            "normal": (0.1, 0.5),
            "mci": (0.5, 1.5),
            "ad": (1.5, 4.0)
        }

        # White matter hyperintensities (Fazekas scale 0-3)
        wmh_probs = {
            "normal": [0.7, 0.2, 0.08, 0.02],
            "mci": [0.3, 0.4, 0.2, 0.1],
            "ad": [0.1, 0.3, 0.35, 0.25]
        }

        return {
            **brain_volumes,
            "hippocampal_atrophy_rate": round(self._get_value_in_range(atrophy_rates[stage_key]), 2),
            "ventricular_volume": round(self._get_value_in_range({
                "normal": (2.0, 3.5),
                "mci": (3.5, 5.0),
                "ad": (5.0, 8.0)
            }[stage_key]), 2),
            "cortical_thickness_mm": round(self._get_value_in_range({
                "normal": (2.4, 2.7),
                "mci": (2.1, 2.4),
                "ad": (1.7, 2.1)
            }[stage_key]), 2),
            "white_matter_hyperintensities_fazekas": random.choices([0, 1, 2, 3], wmh_probs[stage_key])[0],
            "amyloid_pet_suvr": round(self._get_value_in_range({
                "normal": (0.8, 1.1),
                "mci": (1.1, 1.4),
                "ad": (1.4, 2.2)
            }[stage_key]), 2),
            "tau_pet_suvr": round(self._get_value_in_range({
                "normal": (0.9, 1.1),
                "mci": (1.1, 1.5),
                "ad": (1.5, 2.5)
            }[stage_key]), 2),
            "fdg_pet_hypometabolism": stage_key != "normal"
        }

    def generate_csf_biomarkers(self, stage: str) -> Dict[str, Any]:
        """Generate CSF biomarker data."""
        stage_key = "ad" if stage in ["mild", "moderate", "severe"] else stage
        if stage_key == "normal":
            stage_key = "normal"
        elif stage_key == "mci":
            stage_key = "mci"
        else:
            stage_key = "ad"

        csf = {}
        for marker, ranges in CSF_BIOMARKERS.items():
            csf[f"csf_{marker}"] = round(self._get_value_in_range(ranges[stage_key]), 1)

        # Calculate ratios
        csf["csf_tau_abeta_ratio"] = round(csf["csf_tau"] / max(1, csf["csf_abeta42"]), 3)
        csf["csf_ptau_abeta_ratio"] = round(csf["csf_ptau181"] / max(1, csf["csf_abeta42"]), 4)

        # AT(N) classification
        csf["atn_classification"] = {
            "amyloid_positive": csf["csf_abeta42"] < 500,
            "tau_positive": csf["csf_ptau181"] > 40,
            "neurodegeneration_positive": csf["csf_tau"] > 300
        }

        return csf

    def generate_medical_history(self, stage: str, age: int) -> Dict[str, Any]:
        """Generate medical history and comorbidities."""
        # Probabilities increase with stage and age
        age_factor = (age - 50) / 50
        stage_factors = {"normal": 0.5, "mci": 0.7, "mild": 0.85, "moderate": 0.95, "severe": 1.0}
        sf = stage_factors[stage]

        return {
            "hypertension": random.random() < (0.3 + 0.3 * age_factor) * sf,
            "diabetes_type2": random.random() < (0.1 + 0.15 * age_factor) * sf,
            "hyperlipidemia": random.random() < (0.25 + 0.2 * age_factor) * sf,
            "cardiovascular_disease": random.random() < (0.15 + 0.2 * age_factor) * sf,
            "stroke_history": random.random() < (0.05 + 0.1 * age_factor) * sf,
            "depression": random.random() < (0.2 * sf + 0.1),
            "anxiety": random.random() < (0.15 * sf + 0.05),
            "sleep_disorders": random.random() < (0.3 * sf),
            "hearing_loss": random.random() < (0.2 + 0.3 * age_factor),
            "vision_impairment": random.random() < (0.15 + 0.25 * age_factor),
            "traumatic_brain_injury": random.random() < 0.08,
            "smoking_history": random.random() < 0.25,
            "alcohol_use": random.choice(["None", "Light", "Moderate", "Heavy"]),
            "bmi": round(random.gauss(26, 5), 1),
            "physical_activity_level": random.choice(["Sedentary", "Light", "Moderate", "Active"])
        }

    def generate_speech_markers(self, stage: str) -> Dict[str, Any]:
        """Generate speech and language analysis data."""
        stage_key = "ad" if stage in ["mild", "moderate", "severe"] else stage
        if stage_key == "normal":
            stage_key = "normal"
        elif stage_key == "mci":
            stage_key = "mci"
        else:
            stage_key = "ad"

        speech = {}
        for marker, ranges in SPEECH_MARKERS.items():
            speech[marker] = round(self._get_value_in_range(ranges[stage_key]), 1)

        # Additional speech features
        speech["vocabulary_richness"] = round(self._get_value_in_range({
            "normal": (0.7, 0.9),
            "mci": (0.5, 0.7),
            "ad": (0.2, 0.5)
        }[stage_key]), 2)

        speech["sentence_complexity"] = round(self._get_value_in_range({
            "normal": (0.6, 0.85),
            "mci": (0.4, 0.6),
            "ad": (0.15, 0.4)
        }[stage_key]), 2)

        speech["coherence_score"] = round(self._get_value_in_range({
            "normal": (0.8, 1.0),
            "mci": (0.6, 0.8),
            "ad": (0.3, 0.6)
        }[stage_key]), 2)

        return speech

    def generate_daily_activities(self, stage: str) -> Dict[str, Any]:
        """Generate daily activity monitoring data."""
        stage_key = "ad" if stage in ["mild", "moderate", "severe"] else stage
        if stage_key == "normal":
            stage_key = "normal"
        elif stage_key == "mci":
            stage_key = "mci"
        else:
            stage_key = "ad"

        activities = {}
        for marker, ranges in ACTIVITY_MARKERS.items():
            activities[marker] = round(self._get_value_in_range(ranges[stage_key]), 2)

        # ADL (Activities of Daily Living) scores
        activities["adl_basic_score"] = round(self._get_value_in_range({
            "normal": (95, 100),
            "mci": (85, 95),
            "ad": (40, 85)
        }[stage_key]), 1)

        activities["adl_instrumental_score"] = round(self._get_value_in_range({
            "normal": (90, 100),
            "mci": (70, 90),
            "ad": (20, 70)
        }[stage_key]), 1)

        # GPS tracking data
        activities["location_visits_per_day"] = int(self._get_value_in_range({
            "normal": (3, 8),
            "mci": (2, 5),
            "ad": (1, 3)
        }[stage_key]))

        activities["time_at_home_percent"] = round(self._get_value_in_range({
            "normal": (40, 60),
            "mci": (60, 80),
            "ad": (80, 98)
        }[stage_key]), 1)

        return activities

    def generate_treatment_data(self, stage: str) -> Dict[str, Any]:
        """Generate treatment and medication data."""
        if stage == "normal":
            return {
                "on_ad_medication": False,
                "medications": [],
                "clinical_trial": random.random() < 0.05,
                "cognitive_therapy": random.random() < 0.1,
                "physical_therapy": False,
                "occupational_therapy": False
            }

        med_probs = {"mci": 0.3, "mild": 0.7, "moderate": 0.9, "severe": 0.95}
        on_meds = random.random() < med_probs[stage]

        medications = []
        if on_meds:
            if stage in ["mci", "mild"]:
                medications.append(random.choice(MEDICATIONS["cholinesterase_inhibitors"]))
            elif stage == "moderate":
                medications.append(random.choice(MEDICATIONS["cholinesterase_inhibitors"]))
                if random.random() < 0.6:
                    medications.append(MEDICATIONS["nmda_antagonists"][0])
            else:  # severe
                if random.random() < 0.5:
                    medications.append(random.choice(MEDICATIONS["combination"]))
                else:
                    medications.extend([
                        random.choice(MEDICATIONS["cholinesterase_inhibitors"]),
                        MEDICATIONS["nmda_antagonists"][0]
                    ])

            # Add supportive medications
            if random.random() < 0.4:
                medications.append(random.choice(MEDICATIONS["supportive"]))

        return {
            "on_ad_medication": on_meds,
            "medications": medications,
            "clinical_trial": random.random() < (0.15 if stage in ["mci", "mild"] else 0.05),
            "cognitive_therapy": random.random() < (0.4 if stage in ["mci", "mild"] else 0.2),
            "physical_therapy": random.random() < (0.3 if stage in ["moderate", "severe"] else 0.1),
            "occupational_therapy": random.random() < (0.4 if stage in ["moderate", "severe"] else 0.15),
            "speech_therapy": random.random() < (0.2 if stage in ["moderate", "severe"] else 0.05),
            "caregiver_support": stage in ["moderate", "severe"] or random.random() < 0.3
        }

    def generate_longitudinal_data(self, stage: str, months: int = 24) -> List[Dict[str, Any]]:
        """Generate longitudinal follow-up data points."""
        data_points = []

        # Progression rates vary by stage
        progression_rates = {
            "normal": 0.02,  # 2% chance of progressing per month
            "mci": 0.04,     # 4% chance
            "mild": 0.03,    # 3% chance
            "moderate": 0.02,
            "severe": 0.01
        }

        stages = ["normal", "mci", "mild", "moderate", "severe"]
        current_stage_idx = stages.index(stage)
        current_stage = stage

        for month in range(0, months + 1, 6):
            # Check for progression
            if random.random() < progression_rates[current_stage] * 6:
                if current_stage_idx < len(stages) - 1:
                    current_stage_idx += 1
                    current_stage = stages[current_stage_idx]

            # Generate scores for this time point
            cognitive = self.generate_cognitive_scores(current_stage)

            data_points.append({
                "months_from_baseline": month,
                "stage": current_stage,
                "mmse": cognitive["mmse_total"],
                "moca": cognitive["moca_total"],
                "cdr": cognitive["cdr_global"],
                "progressed": current_stage != stage
            })

        return data_points

    def generate_patient(self, stage: str = None) -> Dict[str, Any]:
        """Generate a complete patient record."""
        if stage is None:
            stage = random.choices(
                ["normal", "mci", "mild", "moderate", "severe"],
                weights=[0.30, 0.25, 0.20, 0.15, 0.10]
            )[0]

        self.patient_id_counter += 1
        patient_id = f"NS-{self.patient_id_counter:06d}"

        demographics = self.generate_demographics(stage)
        genetic = self.generate_genetic_data(stage)
        cognitive = self.generate_cognitive_scores(stage)
        neuroimaging = self.generate_neuroimaging(stage)
        csf = self.generate_csf_biomarkers(stage)
        medical = self.generate_medical_history(stage, demographics["age"])
        speech = self.generate_speech_markers(stage)
        activities = self.generate_daily_activities(stage)
        treatment = self.generate_treatment_data(stage)
        longitudinal = self.generate_longitudinal_data(stage)

        # Calculate composite risk score
        risk_score = self._calculate_risk_score(
            demographics, genetic, cognitive, neuroimaging, medical
        )

        return {
            "patient_id": patient_id,
            "created_at": datetime.now().isoformat(),
            "demographics": demographics,
            "genetic": genetic,
            "cognitive_assessment": cognitive,
            "neuroimaging": neuroimaging,
            "csf_biomarkers": csf,
            "medical_history": medical,
            "speech_analysis": speech,
            "daily_activities": activities,
            "treatment": treatment,
            "longitudinal_data": longitudinal,
            "risk_assessment": {
                "composite_risk_score": round(risk_score, 3),
                "risk_category": "High" if risk_score > 0.7 else "Moderate" if risk_score > 0.4 else "Low",
                "5_year_progression_probability": round(min(0.95, risk_score * 1.2), 2),
                "recommended_follow_up_months": 3 if risk_score > 0.7 else 6 if risk_score > 0.4 else 12
            }
        }

    def _calculate_risk_score(self, demographics, genetic, cognitive, neuroimaging, medical) -> float:
        """Calculate composite risk score based on multiple factors."""
        score = 0.0

        # Age factor
        age = demographics["age"]
        if age >= 65:
            score += RISK_FACTORS["age"]["weight"] * min(1.0, (age - 65) / 30)

        # Genetic factors
        if genetic["has_apoe4_allele"]:
            score += RISK_FACTORS["apoe4"]["weight"] * (genetic["apoe_risk_multiplier"] / 15)

        if genetic["family_history_alzheimers"]:
            score += RISK_FACTORS["family_history"]["weight"]

        # Education (protective)
        if demographics["education_years"] < 12:
            score += abs(RISK_FACTORS["education_years"]["weight"]) * (12 - demographics["education_years"]) / 12

        # Medical history
        if medical.get("cardiovascular_disease"):
            score += RISK_FACTORS["cardiovascular"]["weight"]
        if medical.get("diabetes_type2"):
            score += RISK_FACTORS["diabetes"]["weight"]
        if medical.get("depression"):
            score += RISK_FACTORS["depression"]["weight"]
        if medical.get("traumatic_brain_injury"):
            score += RISK_FACTORS["head_injury"]["weight"]
        if medical.get("physical_activity_level") == "Sedentary":
            score += RISK_FACTORS["physical_inactivity"]["weight"]

        # Cognitive scores
        mmse = cognitive["mmse_total"]
        if mmse < 24:
            score += 0.3 * (24 - mmse) / 24

        # Neuroimaging
        if neuroimaging["amyloid_pet_suvr"] > 1.2:
            score += 0.15
        if neuroimaging["hippocampus_volume"] < 0.48:
            score += 0.1

        return min(1.0, score)

    def generate_dataset(self, n_patients: int = 10000) -> List[Dict[str, Any]]:
        """Generate a complete dataset with n patients."""
        dataset = []

        # Distribution of stages
        stage_distribution = {
            "normal": int(n_patients * 0.30),
            "mci": int(n_patients * 0.25),
            "mild": int(n_patients * 0.20),
            "moderate": int(n_patients * 0.15),
            "severe": int(n_patients * 0.10)
        }

        for stage, count in stage_distribution.items():
            for _ in range(count):
                patient = self.generate_patient(stage)
                dataset.append(patient)

        random.shuffle(dataset)
        return dataset


def generate_and_save_dataset(n_patients: int = 50000, output_file: str = "alzheimers_training_data.json"):
    """Generate and save a large dataset."""
    print(f"Generating {n_patients:,} patient records...")

    generator = AlzheimersDatasetGenerator()
    dataset = generator.generate_dataset(n_patients)

    # Add metadata
    output = {
        "metadata": {
            "dataset_name": "NeuroSmriti Alzheimer's Training Dataset",
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "total_records": len(dataset),
            "description": "Comprehensive synthetic dataset for Alzheimer's detection and progression prediction",
            "sources": [
                "ADNI (Alzheimer's Disease Neuroimaging Initiative)",
                "OASIS (Open Access Series of Imaging Studies)",
                "NACC (National Alzheimer's Coordinating Center)",
                "Clinical research literature and meta-analyses"
            ],
            "features": {
                "demographics": 6,
                "genetic": 8,
                "cognitive": 25,
                "neuroimaging": 15,
                "csf_biomarkers": 8,
                "medical_history": 15,
                "speech_analysis": 8,
                "daily_activities": 10,
                "treatment": 8,
                "longitudinal": "up to 24 months"
            },
            "stage_distribution": {
                "normal": sum(1 for p in dataset if p["cognitive_assessment"]["diagnosis_stage"] == "normal"),
                "mci": sum(1 for p in dataset if p["cognitive_assessment"]["diagnosis_stage"] == "mci"),
                "mild": sum(1 for p in dataset if p["cognitive_assessment"]["diagnosis_stage"] == "mild"),
                "moderate": sum(1 for p in dataset if p["cognitive_assessment"]["diagnosis_stage"] == "moderate"),
                "severe": sum(1 for p in dataset if p["cognitive_assessment"]["diagnosis_stage"] == "severe")
            }
        },
        "data": dataset
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Dataset saved to {output_file}")
    print(f"File size: {len(json.dumps(output)) / 1024 / 1024:.2f} MB")

    return output


if __name__ == "__main__":
    # Generate a sample dataset
    generate_and_save_dataset(n_patients=1000, output_file="sample_alzheimers_data.json")
