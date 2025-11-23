"""
Large-Scale Alzheimer's Disease Training Dataset Generator
Generates 400,000+ synthetic patient records for AI training

Based on clinical research from:
- ADNI (Alzheimer's Disease Neuroimaging Initiative)
- OASIS (Open Access Series of Imaging Studies)
- NACC (National Alzheimer's Coordinating Center)
- UK Biobank
- AIBL (Australian Imaging, Biomarker & Lifestyle)
- WHO Dementia Guidelines
- Alzheimer's Association Research Data
"""

import json
import random
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

# =====================================================
# EXPANDED CLINICAL REFERENCE DATA
# =====================================================

# Extended Names Database for realistic patient generation
MALE_FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
    "Kenneth", "Kevin", "Brian", "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan",
    "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
    "Benjamin", "Samuel", "Raymond", "Gregory", "Frank", "Alexander", "Patrick", "Raymond", "Jack", "Dennis",
    "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry", "Douglas", "Zachary", "Peter",
    "Kyle", "Walter", "Ethan", "Jeremy", "Harold", "Keith", "Christian", "Roger", "Noah", "Gerald",
    "Carl", "Terry", "Sean", "Austin", "Arthur", "Lawrence", "Jesse", "Dylan", "Bryan", "Joe",
    "Jordan", "Billy", "Bruce", "Albert", "Willie", "Gabriel", "Logan", "Alan", "Juan", "Wayne",
    "Elijah", "Randy", "Roy", "Vincent", "Ralph", "Eugene", "Russell", "Bobby", "Mason", "Philip"
]

FEMALE_FIRST_NAMES = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen",
    "Lisa", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Kimberly", "Emily", "Donna", "Michelle",
    "Dorothy", "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia",
    "Kathleen", "Amy", "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma", "Nicole", "Helen",
    "Samantha", "Katherine", "Christine", "Debra", "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather",
    "Diane", "Ruth", "Julie", "Olivia", "Joyce", "Virginia", "Victoria", "Kelly", "Lauren", "Christina",
    "Joan", "Evelyn", "Judith", "Megan", "Andrea", "Cheryl", "Hannah", "Jacqueline", "Martha", "Gloria",
    "Teresa", "Ann", "Sara", "Madison", "Frances", "Kathryn", "Janice", "Jean", "Abigail", "Alice",
    "Judy", "Sophia", "Grace", "Denise", "Amber", "Doris", "Marilyn", "Danielle", "Beverly", "Isabella",
    "Theresa", "Diana", "Natalie", "Brittany", "Charlotte", "Marie", "Kayla", "Alexis", "Lori", "Julia"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
]

# CDR Stages with detailed descriptions
CDR_STAGES = {
    0: {"name": "Normal", "description": "No cognitive impairment"},
    0.5: {"name": "Very Mild Dementia", "description": "Questionable cognitive impairment, possible MCI"},
    1: {"name": "Mild Dementia", "description": "Mild cognitive impairment affecting daily life"},
    2: {"name": "Moderate Dementia", "description": "Moderate cognitive impairment, needs assistance"},
    3: {"name": "Severe Dementia", "description": "Severe cognitive impairment, dependent on others"}
}

# Cognitive Score Ranges
SCORE_RANGES = {
    "mmse": {
        "normal": (27, 30), "mci": (24, 27), "mild": (20, 24),
        "moderate": (10, 20), "severe": (0, 10)
    },
    "moca": {
        "normal": (26, 30), "mci": (22, 26), "mild": (17, 22),
        "moderate": (10, 17), "severe": (0, 10)
    },
    "adas_cog": {
        "normal": (0, 10), "mci": (10, 18), "mild": (18, 30),
        "moderate": (30, 50), "severe": (50, 70)
    },
    "faq": {
        "normal": (0, 2), "mci": (2, 8), "mild": (8, 15),
        "moderate": (15, 25), "severe": (25, 30)
    }
}

# APOE Genotypes
APOE_DATA = {
    "e2/e2": {"freq": 0.01, "risk": 0.6, "onset_modifier": 5},
    "e2/e3": {"freq": 0.11, "risk": 0.6, "onset_modifier": 3},
    "e2/e4": {"freq": 0.02, "risk": 2.6, "onset_modifier": -2},
    "e3/e3": {"freq": 0.60, "risk": 1.0, "onset_modifier": 0},
    "e3/e4": {"freq": 0.21, "risk": 3.2, "onset_modifier": -5},
    "e4/e4": {"freq": 0.05, "risk": 14.9, "onset_modifier": -10}
}

# Brain Regions with volume ranges (normalized)
BRAIN_VOLUMES = {
    "hippocampus_left": {"normal": (3200, 3800), "mci": (2800, 3200), "ad": (2200, 2800)},
    "hippocampus_right": {"normal": (3300, 3900), "mci": (2900, 3300), "ad": (2300, 2900)},
    "entorhinal_left": {"normal": (1800, 2200), "mci": (1500, 1800), "ad": (1000, 1500)},
    "entorhinal_right": {"normal": (1900, 2300), "mci": (1600, 1900), "ad": (1100, 1600)},
    "amygdala_left": {"normal": (1400, 1700), "mci": (1200, 1400), "ad": (900, 1200)},
    "amygdala_right": {"normal": (1450, 1750), "mci": (1250, 1450), "ad": (950, 1250)},
    "temporal_lobe": {"normal": (80000, 95000), "mci": (70000, 80000), "ad": (55000, 70000)},
    "frontal_lobe": {"normal": (120000, 140000), "mci": (105000, 120000), "ad": (85000, 105000)},
    "parietal_lobe": {"normal": (75000, 90000), "mci": (65000, 75000), "ad": (50000, 65000)},
    "occipital_lobe": {"normal": (40000, 50000), "mci": (35000, 40000), "ad": (28000, 35000)},
    "total_brain": {"normal": (1100000, 1300000), "mci": (1000000, 1100000), "ad": (850000, 1000000)},
    "ventricular_volume": {"normal": (20000, 35000), "mci": (35000, 55000), "ad": (55000, 90000)}
}

# CSF Biomarkers (pg/mL)
CSF_MARKERS = {
    "abeta42": {"normal": (500, 1200), "mci": (350, 500), "ad": (150, 350)},
    "abeta40": {"normal": (8000, 15000), "mci": (7000, 10000), "ad": (5000, 8000)},
    "total_tau": {"normal": (100, 300), "mci": (300, 500), "ad": (500, 1200)},
    "ptau181": {"normal": (15, 40), "mci": (40, 70), "ad": (70, 150)},
    "ptau217": {"normal": (5, 15), "mci": (15, 40), "ad": (40, 100)},
    "nfl": {"normal": (200, 600), "mci": (600, 1200), "ad": (1200, 3000)}
}

# Blood Biomarkers (newer research)
BLOOD_MARKERS = {
    "plasma_abeta42_40_ratio": {"normal": (0.08, 0.12), "mci": (0.06, 0.08), "ad": (0.03, 0.06)},
    "plasma_ptau181": {"normal": (1, 3), "mci": (3, 6), "ad": (6, 15)},
    "plasma_ptau217": {"normal": (0.5, 2), "mci": (2, 5), "ad": (5, 20)},
    "plasma_nfl": {"normal": (10, 30), "mci": (30, 60), "ad": (60, 150)},
    "plasma_gfap": {"normal": (50, 150), "mci": (150, 300), "ad": (300, 600)}
}

# Ethnicities with AD risk modifiers
ETHNICITIES = {
    "White/Caucasian": {"freq": 0.58, "risk": 1.0},
    "Black/African American": {"freq": 0.13, "risk": 1.5},
    "Hispanic/Latino": {"freq": 0.18, "risk": 1.3},
    "Asian": {"freq": 0.06, "risk": 0.8},
    "Native American": {"freq": 0.02, "risk": 1.2},
    "Pacific Islander": {"freq": 0.01, "risk": 0.9},
    "Mixed/Other": {"freq": 0.02, "risk": 1.0}
}

# Medications
MEDICATIONS = {
    "cholinesterase_inhibitors": [
        "Donepezil (Aricept) 5mg", "Donepezil (Aricept) 10mg", "Donepezil (Aricept) 23mg",
        "Rivastigmine (Exelon) oral", "Rivastigmine (Exelon) patch",
        "Galantamine (Razadyne) IR", "Galantamine (Razadyne) ER"
    ],
    "nmda_antagonists": ["Memantine (Namenda) IR", "Memantine (Namenda) XR"],
    "combination": ["Namzaric (Memantine/Donepezil)"],
    "new_therapies": ["Lecanemab (Leqembi)", "Aducanumab (Aduhelm)", "Donanemab (pending)"],
    "supportive": [
        "SSRI Antidepressant", "SNRI Antidepressant", "Atypical Antipsychotic",
        "Benzodiazepine", "Sleep Aid", "Mood Stabilizer", "Anti-anxiety"
    ]
}

# Comorbidities
COMORBIDITIES = [
    "Hypertension", "Type 2 Diabetes", "Hyperlipidemia", "Coronary Artery Disease",
    "Atrial Fibrillation", "Congestive Heart Failure", "Stroke/TIA", "Peripheral Vascular Disease",
    "COPD", "Chronic Kidney Disease", "Hypothyroidism", "Osteoarthritis",
    "Osteoporosis", "Depression", "Anxiety", "Sleep Apnea", "Hearing Loss", "Vision Impairment"
]


class FastDatasetGenerator:
    """Optimized generator for large-scale dataset creation."""

    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)

    def _rand_range(self, r: Tuple[float, float], noise: float = 0.05) -> float:
        """Get random value in range with optional noise."""
        val = random.uniform(r[0], r[1])
        return val + random.gauss(0, (r[1] - r[0]) * noise)

    def _weighted_choice(self, options: Dict[str, Dict], key: str = "freq") -> str:
        """Weighted random choice."""
        items = list(options.keys())
        weights = [options[k][key] for k in items]
        return random.choices(items, weights=weights)[0]

    def generate_patient(self, patient_id: int, stage: str = None) -> Dict[str, Any]:
        """Generate a single patient record."""
        # Determine stage
        if stage is None:
            stage = random.choices(
                ["normal", "mci", "mild", "moderate", "severe"],
                weights=[0.30, 0.25, 0.20, 0.15, 0.10]
            )[0]

        stage_key = "ad" if stage in ["mild", "moderate", "severe"] else stage
        if stage_key not in ["normal", "mci"]:
            stage_key = "ad"

        # Demographics
        age_ranges = {
            "normal": (55, 78), "mci": (60, 82), "mild": (65, 88),
            "moderate": (70, 92), "severe": (75, 98)
        }
        age = int(self._rand_range(age_ranges[stage]))

        # Gender (females more prevalent in AD)
        female_prob = {"normal": 0.50, "mci": 0.53, "mild": 0.56, "moderate": 0.58, "severe": 0.60}
        is_female = random.random() < female_prob[stage]

        first_name = random.choice(FEMALE_FIRST_NAMES if is_female else MALE_FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        ethnicity = self._weighted_choice(ETHNICITIES)

        education = max(0, int(random.gauss(
            {"normal": 14, "mci": 13, "mild": 12, "moderate": 11, "severe": 10}[stage], 3
        )))

        # Genetics
        apoe = self._weighted_choice(APOE_DATA)

        # Cognitive Scores
        mmse = round(self._rand_range(SCORE_RANGES["mmse"][stage]), 1)
        moca = round(self._rand_range(SCORE_RANGES["moca"][stage]), 1)
        adas_cog = round(self._rand_range(SCORE_RANGES["adas_cog"][stage]), 1)
        faq = round(self._rand_range(SCORE_RANGES["faq"][stage]), 1)

        cdr_map = {"normal": 0, "mci": 0.5, "mild": 1, "moderate": 2, "severe": 3}
        cdr = cdr_map[stage]

        # Brain Volumes
        brain_data = {}
        for region, ranges in BRAIN_VOLUMES.items():
            brain_data[region] = round(self._rand_range(ranges[stage_key]))

        # CSF Biomarkers
        csf_data = {}
        for marker, ranges in CSF_MARKERS.items():
            csf_data[f"csf_{marker}"] = round(self._rand_range(ranges[stage_key]), 1)

        # Blood Biomarkers
        blood_data = {}
        for marker, ranges in BLOOD_MARKERS.items():
            blood_data[marker] = round(self._rand_range(ranges[stage_key]), 3)

        # PET Imaging
        amyloid_suvr = round(self._rand_range(
            {"normal": (0.8, 1.1), "mci": (1.1, 1.4), "ad": (1.4, 2.2)}[stage_key]
        ), 2)
        tau_suvr = round(self._rand_range(
            {"normal": (0.9, 1.1), "mci": (1.1, 1.5), "ad": (1.5, 2.5)}[stage_key]
        ), 2)
        fdg_hypometabolism = stage_key != "normal"

        # Medical History
        age_factor = (age - 50) / 50
        stage_factor = {"normal": 0.5, "mci": 0.7, "mild": 0.85, "moderate": 0.95, "severe": 1.0}[stage]

        comorbidities = []
        for condition in COMORBIDITIES:
            prob = 0.1 + 0.2 * age_factor * stage_factor
            if random.random() < prob:
                comorbidities.append(condition)

        # Treatment
        medications = []
        if stage != "normal":
            if random.random() < {"mci": 0.3, "mild": 0.7, "moderate": 0.9, "severe": 0.95}[stage]:
                medications.append(random.choice(MEDICATIONS["cholinesterase_inhibitors"]))
                if stage in ["moderate", "severe"] and random.random() < 0.6:
                    medications.append(random.choice(MEDICATIONS["nmda_antagonists"]))
                if random.random() < 0.1:
                    medications.append(random.choice(MEDICATIONS["new_therapies"]))

        # Speech Markers
        wpm = round(self._rand_range(
            {"normal": (120, 150), "mci": (90, 120), "ad": (50, 90)}[stage_key]
        ))
        pause_freq = round(self._rand_range(
            {"normal": (2, 5), "mci": (5, 10), "ad": (10, 20)}[stage_key]
        ), 1)
        word_finding = round(self._rand_range(
            {"normal": (0, 2), "mci": (2, 5), "ad": (5, 15)}[stage_key]
        ), 1)

        # Daily Activities
        adl_basic = round(self._rand_range(
            {"normal": (95, 100), "mci": (85, 95), "ad": (40, 85)}[stage_key]
        ), 1)
        adl_instrumental = round(self._rand_range(
            {"normal": (90, 100), "mci": (70, 90), "ad": (20, 70)}[stage_key]
        ), 1)
        sleep_hours = round(self._rand_range(
            {"normal": (6.5, 8.5), "mci": (5, 7), "ad": (4, 10)}[stage_key]
        ), 1)

        # Risk Score Calculation
        risk_score = 0.0
        if age >= 65:
            risk_score += 0.25 * min(1.0, (age - 65) / 30)
        if "e4" in apoe:
            risk_score += 0.20 * (APOE_DATA[apoe]["risk"] / 15)
        if education < 12:
            risk_score += 0.10 * (12 - education) / 12
        if mmse < 24:
            risk_score += 0.3 * (24 - mmse) / 24
        if amyloid_suvr > 1.2:
            risk_score += 0.15
        risk_score = min(1.0, risk_score)

        # Build record
        record = {
            "patient_id": f"NS-{patient_id:07d}",
            "demographics": {
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
                "gender": "Female" if is_female else "Male",
                "ethnicity": ethnicity,
                "education_years": education,
                "marital_status": random.choice(["Married", "Single", "Widowed", "Divorced"]),
                "living_situation": random.choice(["Independent", "With Family", "Assisted Living", "Nursing Home"]),
                "insurance_type": random.choice(["Medicare", "Private", "Medicaid", "Medicare Advantage"])
            },
            "genetics": {
                "apoe_genotype": apoe,
                "has_apoe4": "e4" in apoe,
                "risk_multiplier": APOE_DATA[apoe]["risk"],
                "family_history_ad": random.random() < {"normal": 0.15, "mci": 0.25, "mild": 0.35, "moderate": 0.40, "severe": 0.45}[stage],
                "family_history_dementia": random.random() < 0.3
            },
            "cognitive_scores": {
                "mmse_total": mmse,
                "moca_total": moca,
                "adas_cog_13": adas_cog,
                "faq_total": faq,
                "cdr_global": cdr,
                "cdr_sob": round(cdr * 3 + random.uniform(-0.5, 0.5), 1),
                "diagnosis_stage": stage,
                "diagnosis_label": CDR_STAGES[cdr]["name"]
            },
            "neuroimaging": {
                **brain_data,
                "amyloid_pet_suvr": amyloid_suvr,
                "tau_pet_suvr": tau_suvr,
                "fdg_hypometabolism": fdg_hypometabolism,
                "mri_quality": random.choice(["Good", "Excellent", "Fair"]),
                "scan_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
            },
            "biomarkers": {
                "csf": csf_data,
                "blood": blood_data,
                "csf_abeta42_40_ratio": round(csf_data["csf_abeta42"] / max(1, csf_data.get("csf_abeta40", 10000)), 4),
                "csf_ptau_abeta_ratio": round(csf_data["csf_ptau181"] / max(1, csf_data["csf_abeta42"]), 4),
                "amyloid_positive": csf_data["csf_abeta42"] < 500,
                "tau_positive": csf_data["csf_ptau181"] > 40,
                "neurodegeneration_positive": csf_data["csf_total_tau"] > 300
            },
            "medical_history": {
                "comorbidities": comorbidities,
                "hypertension": "Hypertension" in comorbidities,
                "diabetes": "Type 2 Diabetes" in comorbidities,
                "cardiovascular": any(c in comorbidities for c in ["Coronary Artery Disease", "Atrial Fibrillation", "Congestive Heart Failure"]),
                "stroke_history": "Stroke/TIA" in comorbidities,
                "depression": "Depression" in comorbidities,
                "head_injury": random.random() < 0.08,
                "smoking": random.choice(["Never", "Former", "Current"]),
                "alcohol_use": random.choice(["None", "Light", "Moderate", "Heavy"]),
                "bmi": round(random.gauss(26, 5), 1),
                "physical_activity": random.choice(["Sedentary", "Light", "Moderate", "Active"])
            },
            "speech_analysis": {
                "words_per_minute": wpm,
                "pause_frequency": pause_freq,
                "word_finding_difficulty": word_finding,
                "semantic_errors": round(self._rand_range({"normal": (0, 1), "mci": (1, 3), "ad": (3, 10)}[stage_key]), 1),
                "vocabulary_richness": round(self._rand_range({"normal": (0.7, 0.9), "mci": (0.5, 0.7), "ad": (0.2, 0.5)}[stage_key]), 2),
                "coherence_score": round(self._rand_range({"normal": (0.8, 1.0), "mci": (0.6, 0.8), "ad": (0.3, 0.6)}[stage_key]), 2)
            },
            "daily_activities": {
                "adl_basic_score": adl_basic,
                "adl_instrumental_score": adl_instrumental,
                "sleep_hours": sleep_hours,
                "sleep_quality": random.choice(["Poor", "Fair", "Good", "Excellent"]),
                "medication_adherence": round(self._rand_range({"normal": (0.9, 1.0), "mci": (0.7, 0.9), "ad": (0.3, 0.7)}[stage_key]), 2),
                "social_interactions_weekly": int(self._rand_range({"normal": (5, 15), "mci": (2, 8), "ad": (0, 4)}[stage_key])),
                "phone_usage_daily_minutes": int(self._rand_range({"normal": (30, 120), "mci": (15, 45), "ad": (0, 20)}[stage_key])),
                "wandering_incidents_monthly": int(self._rand_range({"normal": (0, 0), "mci": (0, 1), "ad": (1, 5)}[stage_key]))
            },
            "treatment": {
                "medications": medications,
                "on_cholinesterase_inhibitor": any("Donepezil" in m or "Rivastigmine" in m or "Galantamine" in m for m in medications),
                "on_memantine": any("Memantine" in m or "Namzaric" in m for m in medications),
                "on_new_therapy": any(m in str(medications) for m in ["Lecanemab", "Aducanumab", "Donanemab"]),
                "cognitive_therapy": random.random() < (0.4 if stage in ["mci", "mild"] else 0.2),
                "physical_therapy": random.random() < (0.3 if stage in ["moderate", "severe"] else 0.1),
                "occupational_therapy": random.random() < (0.4 if stage in ["moderate", "severe"] else 0.15),
                "in_clinical_trial": random.random() < (0.15 if stage in ["mci", "mild"] else 0.05),
                "caregiver_support": stage in ["moderate", "severe"] or random.random() < 0.3
            },
            "risk_assessment": {
                "composite_risk_score": round(risk_score, 3),
                "risk_category": "High" if risk_score > 0.7 else "Moderate" if risk_score > 0.4 else "Low",
                "progression_risk_5yr": round(min(0.95, risk_score * 1.2), 2),
                "recommended_followup_months": 3 if risk_score > 0.7 else 6 if risk_score > 0.4 else 12
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "data_version": "2.0",
                "synthetic": True
            }
        }

        return record


def generate_batch(args):
    """Generate a batch of patients (for parallel processing)."""
    start_id, count, seed = args
    gen = FastDatasetGenerator(seed=seed)
    return [gen.generate_patient(start_id + i) for i in range(count)]


def generate_large_dataset(
    total_patients: int = 400000,
    output_json: str = "alzheimers_400k_dataset.json",
    output_csv: str = "alzheimers_400k_dataset.csv",
    batch_size: int = 10000,
    num_workers: int = None
):
    """Generate a large dataset with parallel processing."""
    if num_workers is None:
        num_workers = max(1, multiprocessing.cpu_count() - 1)

    print(f"=" * 60)
    print(f"NeuroSmriti Large-Scale Dataset Generator")
    print(f"=" * 60)
    print(f"Target: {total_patients:,} patient records")
    print(f"Workers: {num_workers}")
    print(f"Batch size: {batch_size:,}")
    print()

    start_time = datetime.now()
    all_patients = []

    # Create batches
    batches = []
    for i in range(0, total_patients, batch_size):
        count = min(batch_size, total_patients - i)
        batches.append((i, count, i))  # (start_id, count, seed)

    print(f"Processing {len(batches)} batches...")

    # Process batches
    completed = 0
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for batch_results in executor.map(generate_batch, batches):
            all_patients.extend(batch_results)
            completed += len(batch_results)
            pct = completed / total_patients * 100
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = completed / elapsed if elapsed > 0 else 0
            eta = (total_patients - completed) / rate if rate > 0 else 0
            print(f"\rProgress: {completed:,}/{total_patients:,} ({pct:.1f}%) | Rate: {rate:.0f}/sec | ETA: {eta:.0f}s", end="", flush=True)

    print(f"\n\nGeneration complete! Time: {(datetime.now() - start_time).total_seconds():.1f}s")

    # Calculate statistics
    stage_counts = {"normal": 0, "mci": 0, "mild": 0, "moderate": 0, "severe": 0}
    gender_counts = {"Male": 0, "Female": 0}
    for p in all_patients:
        stage_counts[p["cognitive_scores"]["diagnosis_stage"]] += 1
        gender_counts[p["demographics"]["gender"]] += 1

    # Create metadata
    metadata = {
        "dataset_name": "NeuroSmriti Alzheimer's Training Dataset v2.0",
        "version": "2.0.0",
        "generated_at": datetime.now().isoformat(),
        "total_records": len(all_patients),
        "description": "Large-scale synthetic dataset for Alzheimer's detection and progression AI models",
        "data_sources": [
            "ADNI (Alzheimer's Disease Neuroimaging Initiative)",
            "OASIS (Open Access Series of Imaging Studies)",
            "NACC (National Alzheimer's Coordinating Center)",
            "UK Biobank",
            "AIBL (Australian Imaging, Biomarker & Lifestyle)",
            "WHO Dementia Guidelines",
            "Alzheimer's Association Research"
        ],
        "feature_groups": {
            "demographics": 9,
            "genetics": 5,
            "cognitive_scores": 8,
            "neuroimaging": 16,
            "csf_biomarkers": 8,
            "blood_biomarkers": 5,
            "medical_history": 12,
            "speech_analysis": 6,
            "daily_activities": 8,
            "treatment": 9,
            "risk_assessment": 4
        },
        "total_features": 90,
        "stage_distribution": stage_counts,
        "gender_distribution": gender_counts,
        "generation_time_seconds": (datetime.now() - start_time).total_seconds()
    }

    # Save JSON
    print(f"\nSaving JSON to {output_json}...")
    json_output = {"metadata": metadata, "data": all_patients}

    with open(output_json, 'w') as f:
        json.dump(json_output, f)

    json_size = os.path.getsize(output_json) / (1024 * 1024)
    print(f"JSON saved: {json_size:.1f} MB")

    # Save flattened CSV for easier analysis
    print(f"Saving CSV to {output_csv}...")

    # Flatten patient records for CSV
    csv_rows = []
    for p in all_patients:
        row = {
            "patient_id": p["patient_id"],
            "age": p["demographics"]["age"],
            "gender": p["demographics"]["gender"],
            "ethnicity": p["demographics"]["ethnicity"],
            "education_years": p["demographics"]["education_years"],
            "apoe_genotype": p["genetics"]["apoe_genotype"],
            "has_apoe4": p["genetics"]["has_apoe4"],
            "family_history_ad": p["genetics"]["family_history_ad"],
            "mmse_total": p["cognitive_scores"]["mmse_total"],
            "moca_total": p["cognitive_scores"]["moca_total"],
            "adas_cog_13": p["cognitive_scores"]["adas_cog_13"],
            "faq_total": p["cognitive_scores"]["faq_total"],
            "cdr_global": p["cognitive_scores"]["cdr_global"],
            "diagnosis_stage": p["cognitive_scores"]["diagnosis_stage"],
            "hippocampus_left": p["neuroimaging"]["hippocampus_left"],
            "hippocampus_right": p["neuroimaging"]["hippocampus_right"],
            "amyloid_pet_suvr": p["neuroimaging"]["amyloid_pet_suvr"],
            "tau_pet_suvr": p["neuroimaging"]["tau_pet_suvr"],
            "csf_abeta42": p["biomarkers"]["csf"]["csf_abeta42"],
            "csf_ptau181": p["biomarkers"]["csf"]["csf_ptau181"],
            "csf_total_tau": p["biomarkers"]["csf"]["csf_total_tau"],
            "amyloid_positive": p["biomarkers"]["amyloid_positive"],
            "tau_positive": p["biomarkers"]["tau_positive"],
            "risk_score": p["risk_assessment"]["composite_risk_score"],
            "risk_category": p["risk_assessment"]["risk_category"]
        }
        csv_rows.append(row)

    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
        writer.writeheader()
        writer.writerows(csv_rows)

    csv_size = os.path.getsize(output_csv) / (1024 * 1024)
    print(f"CSV saved: {csv_size:.1f} MB")

    print(f"\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    print(f"Total Records: {len(all_patients):,}")
    print(f"\nStage Distribution:")
    for stage, count in stage_counts.items():
        print(f"  {stage.capitalize()}: {count:,} ({count/len(all_patients)*100:.1f}%)")
    print(f"\nGender Distribution:")
    for gender, count in gender_counts.items():
        print(f"  {gender}: {count:,} ({count/len(all_patients)*100:.1f}%)")
    print(f"\nOutput Files:")
    print(f"  JSON: {output_json} ({json_size:.1f} MB)")
    print(f"  CSV: {output_csv} ({csv_size:.1f} MB)")
    print("=" * 60)

    return metadata


if __name__ == "__main__":
    # Generate 400K+ patient records
    generate_large_dataset(
        total_patients=420000,  # Slightly over 400K
        output_json="alzheimers_420k_dataset.json",
        output_csv="alzheimers_420k_dataset.csv"
    )
