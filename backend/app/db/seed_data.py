"""
Database Seeding Script for NeuroSmriti
Generates comprehensive patient data, memories, and cognitive assessments
"""

import random
import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
import json

# Sample data for generating realistic patients

MALE_FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan"
]

FEMALE_FIRST_NAMES = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
]

ETHNICITIES = ["Caucasian", "African American", "Hispanic", "Asian", "Native American", "Other"]

MEDICAL_CONDITIONS = [
    "Hypertension", "Type 2 Diabetes", "Heart Disease", "High Cholesterol",
    "Arthritis", "Osteoporosis", "Depression", "Anxiety", "Sleep Apnea",
    "Thyroid Disorder", "GERD", "Chronic Pain"
]

MEDICATIONS = {
    "cholinesterase_inhibitors": ["Donepezil (Aricept)", "Rivastigmine (Exelon)", "Galantamine (Razadyne)"],
    "nmda_antagonists": ["Memantine (Namenda)"],
    "combination": ["Namzaric"],
    "supplements": ["Vitamin E", "Omega-3", "Vitamin D", "B Complex", "Ginkgo Biloba"],
    "other": ["Lexapro", "Zoloft", "Ambien", "Trazodone", "Melatonin"]
}

MEMORY_TYPES = ["person", "event", "place", "skill", "fact"]

RELATIONSHIP_TYPES = [
    "Spouse", "Son", "Daughter", "Grandson", "Granddaughter",
    "Brother", "Sister", "Friend", "Neighbor", "Caregiver"
]

MEMORY_EVENTS = [
    "Wedding Day", "First Child Born", "Graduation", "Retirement Party",
    "50th Anniversary", "First Grandchild Born", "Family Reunion",
    "Trip to Europe", "Moving to New Home", "Career Achievement"
]

MEMORY_PLACES = [
    "Childhood Home", "First House", "Favorite Vacation Spot", "Wedding Venue",
    "Workplace", "Church/Temple", "Parent's House", "School", "University"
]

STAGE_DESCRIPTIONS = {
    0: "Normal Cognition",
    1: "Very Mild Decline",
    2: "Mild Decline (MCI)",
    3: "Moderate Decline (Early AD)",
    4: "Moderately Severe Decline",
    5: "Severe Decline",
    6: "Very Severe Decline",
    7: "End Stage"
}


def generate_patient_id() -> str:
    """Generate unique patient ID"""
    return f"NS-{random.randint(100000, 999999)}"


def generate_phone() -> str:
    """Generate random US phone number"""
    return f"({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"


def generate_birth_date(min_age: int = 55, max_age: int = 95) -> date:
    """Generate birth date for given age range"""
    today = date.today()
    age = random.randint(min_age, max_age)
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    return date(birth_year, birth_month, birth_day)


def generate_diagnosis_date(birth_date: date, stage: int) -> date:
    """Generate diagnosis date based on stage"""
    today = date.today()
    age_at_diagnosis = random.randint(60, 85)
    diagnosis_year = birth_date.year + age_at_diagnosis

    if diagnosis_year >= today.year:
        diagnosis_year = today.year - random.randint(1, 5)

    return date(
        diagnosis_year,
        random.randint(1, 12),
        random.randint(1, 28)
    )


def generate_cognitive_scores(stage: int) -> Dict[str, Any]:
    """Generate cognitive scores based on Alzheimer's stage"""
    # MMSE ranges by stage (0-30, higher is better)
    mmse_ranges = {
        0: (27, 30), 1: (25, 28), 2: (22, 26), 3: (18, 23),
        4: (13, 19), 5: (8, 14), 6: (3, 9), 7: (0, 4)
    }

    # MoCA ranges (0-30, higher is better)
    moca_ranges = {
        0: (26, 30), 1: (23, 27), 2: (19, 24), 3: (14, 20),
        4: (10, 15), 5: (5, 11), 6: (2, 6), 7: (0, 3)
    }

    # CDR ranges (0-3, lower is better)
    cdr_ranges = {
        0: (0, 0), 1: (0.5, 0.5), 2: (0.5, 1), 3: (1, 1.5),
        4: (1.5, 2), 5: (2, 2.5), 6: (2.5, 3), 7: (3, 3)
    }

    mmse = random.randint(*mmse_ranges.get(stage, (15, 25)))
    moca = random.randint(*moca_ranges.get(stage, (15, 25)))
    cdr_min, cdr_max = cdr_ranges.get(stage, (1, 2))
    cdr = round(random.uniform(cdr_min, cdr_max), 1)

    return {
        "mmse_score": mmse,
        "moca_score": moca,
        "cdr_score": cdr,
        "last_assessment": datetime.now().isoformat()
    }


def generate_medical_history() -> Dict[str, Any]:
    """Generate medical history"""
    num_conditions = random.randint(0, 5)
    conditions = random.sample(MEDICAL_CONDITIONS, num_conditions)

    return {
        "conditions": conditions,
        "allergies": random.sample(["Penicillin", "Sulfa", "Latex", "None"], 1),
        "surgeries": random.sample(["None", "Hip Replacement", "Knee Surgery", "Cataract", "Heart Bypass"], random.randint(0, 2)),
        "family_history": {
            "alzheimers": random.random() < 0.35,
            "dementia": random.random() < 0.40,
            "heart_disease": random.random() < 0.45,
            "diabetes": random.random() < 0.30
        }
    }


def generate_medications(stage: int) -> List[Dict[str, Any]]:
    """Generate medication list based on stage"""
    medications = []

    # Alzheimer's medications based on stage
    if stage >= 2:
        med = random.choice(MEDICATIONS["cholinesterase_inhibitors"])
        medications.append({
            "name": med,
            "dosage": f"{random.choice([5, 10, 23])}mg",
            "frequency": "Once daily",
            "time": "Evening"
        })

    if stage >= 4:
        medications.append({
            "name": MEDICATIONS["nmda_antagonists"][0],
            "dosage": "10mg",
            "frequency": "Twice daily",
            "time": "Morning and Evening"
        })

    # Add supplements
    num_supplements = random.randint(1, 3)
    for supp in random.sample(MEDICATIONS["supplements"], num_supplements):
        medications.append({
            "name": supp,
            "dosage": "As directed",
            "frequency": "Once daily",
            "time": "Morning"
        })

    return medications


def generate_emergency_contact(gender: str) -> Dict[str, Any]:
    """Generate emergency contact"""
    relationship = random.choice(["Son", "Daughter", "Spouse", "Sibling"])

    if relationship in ["Son", "Spouse"] and gender == "Female":
        contact_name = f"{random.choice(MALE_FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    elif relationship in ["Daughter", "Spouse"] and gender == "Male":
        contact_name = f"{random.choice(FEMALE_FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    else:
        contact_name = f"{random.choice(MALE_FIRST_NAMES + FEMALE_FIRST_NAMES)} {random.choice(LAST_NAMES)}"

    return {
        "name": contact_name,
        "relationship": relationship,
        "phone": generate_phone(),
        "email": f"{contact_name.lower().replace(' ', '.')}@email.com",
        "is_primary": True
    }


def generate_memories(patient_name: str, num_memories: int = 10) -> List[Dict[str, Any]]:
    """Generate memory entries for a patient"""
    memories = []

    # Generate family member memories
    for _ in range(min(5, num_memories)):
        relationship = random.choice(RELATIONSHIP_TYPES)
        is_male = relationship in ["Son", "Grandson", "Brother", "Spouse"] if random.random() > 0.5 else False
        name = random.choice(MALE_FIRST_NAMES if is_male else FEMALE_FIRST_NAMES)

        memories.append({
            "type": "person",
            "title": f"{name} ({relationship})",
            "description": f"{relationship} of {patient_name}",
            "strength": random.randint(40, 100),
            "importance": random.choice(["high", "medium", "high"]),
            "last_reviewed": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "details": {
                "name": name,
                "relationship": relationship,
                "key_facts": [
                    f"Born in {random.randint(1950, 2010)}",
                    f"Lives in {random.choice(['Boston', 'New York', 'Chicago', 'Los Angeles', 'Charlotte'])}"
                ]
            }
        })

    # Generate event memories
    for event in random.sample(MEMORY_EVENTS, min(3, len(MEMORY_EVENTS))):
        memories.append({
            "type": "event",
            "title": event,
            "description": f"Important life event: {event}",
            "strength": random.randint(50, 100),
            "importance": random.choice(["high", "medium"]),
            "last_reviewed": (datetime.now() - timedelta(days=random.randint(0, 60))).isoformat(),
            "details": {
                "date": f"{random.randint(1960, 2020)}",
                "location": random.choice(["Church", "Home", "Beach", "Garden", "Hotel"])
            }
        })

    # Generate place memories
    for place in random.sample(MEMORY_PLACES, min(2, len(MEMORY_PLACES))):
        memories.append({
            "type": "place",
            "title": place,
            "description": f"Significant location: {place}",
            "strength": random.randint(30, 90),
            "importance": random.choice(["high", "medium", "low"]),
            "last_reviewed": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat(),
            "details": {
                "address": f"{random.randint(100, 9999)} {random.choice(['Oak', 'Maple', 'Main', 'Park', 'Lake'])} Street",
                "city": random.choice(["Springfield", "Charlotte", "Boston", "Denver"])
            }
        })

    return memories


def generate_patient(gender: str = None) -> Dict[str, Any]:
    """Generate a complete patient record"""
    if gender is None:
        gender = random.choice(["Male", "Female"])

    first_name = random.choice(MALE_FIRST_NAMES if gender == "Male" else FEMALE_FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    full_name = f"{first_name} {last_name}"

    # Stage distribution (weighted towards earlier stages)
    stage = random.choices(
        [0, 1, 2, 3, 4, 5, 6, 7],
        weights=[15, 15, 20, 20, 15, 8, 5, 2]
    )[0]

    birth_date = generate_birth_date()
    cognitive = generate_cognitive_scores(stage)

    patient = {
        "id": str(uuid.uuid4()),
        "patient_id": generate_patient_id(),
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "date_of_birth": birth_date.isoformat(),
        "age": (date.today() - birth_date).days // 365,
        "ethnicity": random.choice(ETHNICITIES),
        "phone": generate_phone(),
        "email": f"{first_name.lower()}.{last_name.lower()}@email.com",
        "current_stage": stage,
        "stage_description": STAGE_DESCRIPTIONS[stage],
        "diagnosis_date": generate_diagnosis_date(birth_date, stage).isoformat() if stage > 0 else None,
        "mmse_score": cognitive["mmse_score"],
        "moca_score": cognitive["moca_score"],
        "cdr_score": cognitive["cdr_score"],
        "medical_history": generate_medical_history(),
        "medications": generate_medications(stage),
        "emergency_contact": generate_emergency_contact(gender),
        "memories": generate_memories(full_name),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    return patient


def generate_dataset(num_patients: int = 100) -> List[Dict[str, Any]]:
    """Generate a dataset of patients"""
    patients = []

    # Ensure balanced gender distribution
    num_male = num_patients // 2
    num_female = num_patients - num_male

    for _ in range(num_male):
        patients.append(generate_patient("Male"))

    for _ in range(num_female):
        patients.append(generate_patient("Female"))

    random.shuffle(patients)
    return patients


def get_seed_sql(num_patients: int = 50) -> str:
    """Generate SQL for seeding the database"""
    patients = generate_dataset(num_patients)

    sql_statements = []

    # Create a demo user first
    demo_user_id = str(uuid.uuid4())
    sql_statements.append(f"""
INSERT INTO users (id, email, hashed_password, full_name, role, is_active, created_at, updated_at)
VALUES (
    '{demo_user_id}',
    'demo@neurosmriti.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNi/A5wq8FXXa',
    'Demo User',
    'caregiver',
    true,
    NOW(),
    NOW()
) ON CONFLICT (email) DO NOTHING;
""")

    for patient in patients:
        # Insert patient
        sql_statements.append(f"""
INSERT INTO patients (id, caregiver_id, full_name, date_of_birth, gender, phone, email,
    diagnosis_date, current_stage, medical_history, medications, mmse_score, moca_score,
    cdr_score, emergency_contact, created_at, updated_at)
VALUES (
    '{patient["id"]}',
    '{demo_user_id}',
    '{patient["full_name"]}',
    '{patient["date_of_birth"]}',
    '{patient["gender"]}',
    '{patient["phone"]}',
    '{patient["email"]}',
    {f"'{patient['diagnosis_date']}'" if patient['diagnosis_date'] else 'NULL'},
    {patient["current_stage"]},
    '{json.dumps(patient["medical_history"]).replace("'", "''")}',
    '{json.dumps(patient["medications"]).replace("'", "''")}',
    {patient["mmse_score"]},
    {patient["moca_score"]},
    {patient["cdr_score"]},
    '{json.dumps(patient["emergency_contact"]).replace("'", "''")}',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
""")

        # Insert memories
        for memory in patient["memories"]:
            memory_id = str(uuid.uuid4())
            sql_statements.append(f"""
INSERT INTO memories (id, patient_id, memory_type, title, description, memory_metadata,
    importance_score, retention_score, created_at, updated_at)
VALUES (
    '{memory_id}',
    '{patient["id"]}',
    '{memory["type"]}',
    '{memory["title"].replace("'", "''")}',
    '{memory["description"].replace("'", "''")}',
    '{json.dumps(memory["details"]).replace("'", "''")}',
    {random.randint(1, 10)},
    {memory["strength"] / 100.0},
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
""")

    return "\n".join(sql_statements)


if __name__ == "__main__":
    # Generate sample data
    print("Generating seed data...")
    sql = get_seed_sql(100)

    with open("seed_data.sql", "w") as f:
        f.write(sql)

    print(f"Generated seed_data.sql with 100 patients")

    # Also save as JSON for reference
    patients = generate_dataset(100)
    with open("seed_data.json", "w") as f:
        json.dump(patients, f, indent=2)

    print(f"Generated seed_data.json with 100 patients")
