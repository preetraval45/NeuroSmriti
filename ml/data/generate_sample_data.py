"""
Generate sample training data for traditional ML models without heavy dependencies
This creates a smaller dataset for quick testing
"""
import json
import random
import os
from datetime import datetime, timedelta

# Diagnosis stages
DIAGNOSIS_STAGES = ["normal", "mci", "mild_ad", "moderate_ad", "severe_ad"]

# Stage probabilities
STAGE_PROBS = {
    "normal": 0.30,
    "mci": 0.35,
    "mild_ad": 0.20,
    "moderate_ad": 0.10,
    "severe_ad": 0.05
}


def generate_patient(patient_id: int) -> dict:
    """Generate a single synthetic patient record"""

    # Select diagnosis stage
    stage = random.choices(
        list(STAGE_PROBS.keys()),
        weights=list(STAGE_PROBS.values())
    )[0]

    # Demographics
    age = random.randint(55, 95)
    gender = random.choice(["Male", "Female"])
    education_years = random.randint(8, 20)

    # Genetics
    has_apoe4 = random.random() < 0.25  # 25% have APOE4
    family_history_ad = random.random() < 0.30  # 30% have family history

    # Cognitive scores based on stage
    if stage == "normal":
        mmse = random.randint(27, 30)
        moca = random.randint(26, 30)
        adas_cog = random.randint(0, 10)
        faq = random.randint(0, 2)
        cdr = 0.0
    elif stage == "mci":
        mmse = random.randint(24, 27)
        moca = random.randint(22, 26)
        adas_cog = random.randint(10, 18)
        faq = random.randint(2, 8)
        cdr = 0.5
    elif stage == "mild_ad":
        mmse = random.randint(20, 24)
        moca = random.randint(17, 22)
        adas_cog = random.randint(18, 30)
        faq = random.randint(8, 15)
        cdr = 1.0
    elif stage == "moderate_ad":
        mmse = random.randint(10, 20)
        moca = random.randint(10, 17)
        adas_cog = random.randint(30, 50)
        faq = random.randint(15, 25)
        cdr = 2.0
    else:  # severe_ad
        mmse = random.randint(0, 10)
        moca = random.randint(0, 10)
        adas_cog = random.randint(50, 70)
        faq = random.randint(25, 30)
        cdr = 3.0

    # Neuroimaging (volumes in cm³)
    # Hippocampus atrophies with AD progression
    base_hippo_left = random.uniform(2.5, 4.5)
    base_hippo_right = random.uniform(2.5, 4.5)

    stage_atrophy = {
        "normal": 0.0,
        "mci": 0.15,
        "mild_ad": 0.30,
        "moderate_ad": 0.50,
        "severe_ad": 0.70
    }

    atrophy_factor = 1.0 - stage_atrophy[stage]
    hippocampus_left = base_hippo_left * atrophy_factor
    hippocampus_right = base_hippo_right * atrophy_factor

    # PET scan values
    amyloid_pet_suvr = random.uniform(0.8, 1.0) if stage == "normal" else random.uniform(1.2, 2.5)
    tau_pet_suvr = random.uniform(0.9, 1.1) if stage == "normal" else random.uniform(1.3, 3.0)

    # Brain volumes
    total_brain = random.uniform(1000, 1400) * atrophy_factor
    ventricular_volume = random.uniform(20, 40) * (2.0 - atrophy_factor)  # Increases with atrophy

    # CSF Biomarkers
    csf_abeta42 = random.uniform(800, 1200) if stage == "normal" else random.uniform(200, 600)
    csf_ptau181 = random.uniform(15, 30) if stage == "normal" else random.uniform(40, 120)
    csf_total_tau = random.uniform(200, 400) if stage == "normal" else random.uniform(500, 1200)

    amyloid_positive = amyloid_pet_suvr > 1.11
    tau_positive = tau_pet_suvr > 1.25

    # Medical history
    hypertension = random.random() < 0.45
    diabetes = random.random() < 0.20
    cardiovascular = random.random() < 0.30
    depression = random.random() < 0.25

    # Speech analysis
    stage_speech_decline = {
        "normal": 0.0,
        "mci": 0.1,
        "mild_ad": 0.25,
        "moderate_ad": 0.50,
        "severe_ad": 0.75
    }

    base_wpm = random.uniform(100, 160)
    words_per_minute = base_wpm * (1.0 - stage_speech_decline[stage])
    coherence_score = random.uniform(0.8, 1.0) * (1.0 - stage_speech_decline[stage])

    # Daily activities
    adl_basic_score = random.randint(5, 6) if stage in ["normal", "mci"] else random.randint(0, 5)
    adl_instrumental_score = random.randint(6, 8) if stage == "normal" else random.randint(0, 6)

    # Risk score calculation
    risk_factors = 0
    if has_apoe4:
        risk_factors += 0.3
    if family_history_ad:
        risk_factors += 0.2
    if age > 75:
        risk_factors += 0.2
    if hypertension:
        risk_factors += 0.1
    if diabetes:
        risk_factors += 0.1

    risk_score = min(1.0, risk_factors + stage_atrophy[stage])

    # Build patient record
    patient = {
        "patient_id": f"PAT-{patient_id:06d}",
        "demographics": {
            "age": age,
            "gender": gender,
            "education_years": education_years
        },
        "genetics": {
            "has_apoe4": has_apoe4,
            "family_history_ad": family_history_ad
        },
        "cognitive_scores": {
            "mmse_total": mmse,
            "moca_total": moca,
            "adas_cog_13": adas_cog,
            "faq_total": faq,
            "cdr_global": cdr,
            "diagnosis_stage": stage
        },
        "neuroimaging": {
            "hippocampus_left": round(hippocampus_left, 2),
            "hippocampus_right": round(hippocampus_right, 2),
            "amyloid_pet_suvr": round(amyloid_pet_suvr, 2),
            "tau_pet_suvr": round(tau_pet_suvr, 2),
            "total_brain": round(total_brain, 1),
            "ventricular_volume": round(ventricular_volume, 1)
        },
        "biomarkers": {
            "csf": {
                "csf_abeta42": round(csf_abeta42, 1),
                "csf_ptau181": round(csf_ptau181, 1),
                "csf_total_tau": round(csf_total_tau, 1)
            },
            "amyloid_positive": amyloid_positive,
            "tau_positive": tau_positive
        },
        "medical_history": {
            "hypertension": hypertension,
            "diabetes": diabetes,
            "cardiovascular": cardiovascular,
            "depression": depression
        },
        "speech_analysis": {
            "words_per_minute": round(words_per_minute, 1),
            "coherence_score": round(coherence_score, 3)
        },
        "daily_activities": {
            "adl_basic_score": adl_basic_score,
            "adl_instrumental_score": adl_instrumental_score
        },
        "risk_assessment": {
            "composite_risk_score": round(risk_score, 3)
        }
    }

    return patient


def generate_dataset(num_patients: int = 10000, output_file: str = "sample_training_data.json"):
    """Generate complete dataset"""

    print(f"Generating {num_patients} synthetic patients...")

    patients = []
    for i in range(num_patients):
        patient = generate_patient(i)
        patients.append(patient)

        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1}/{num_patients} patients")

    # Save to JSON
    dataset = {
        "metadata": {
            "total_patients": num_patients,
            "generated_date": datetime.now().isoformat(),
            "version": "1.0.0",
            "description": "Synthetic Alzheimer's disease patient dataset for ML training"
        },
        "data": patients
    }

    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"\nDataset saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

    # Print statistics
    stage_counts = {}
    for patient in patients:
        stage = patient["cognitive_scores"]["diagnosis_stage"]
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

    print("\nStage Distribution:")
    for stage, count in sorted(stage_counts.items()):
        print(f"  {stage}: {count} ({count/num_patients*100:.1f}%)")

    return dataset


if __name__ == "__main__":
    # Generate 10,000 patient dataset
    generate_dataset(num_patients=10000, output_file="sample_training_data.json")
    print("\nDone! You can now train models with:")
    print("  python ../train_and_test.py")
