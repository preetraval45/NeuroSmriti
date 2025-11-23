-- NeuroSmriti Database Schema
-- PostgreSQL 16+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector for embedding storage (optional, for future use)
-- CREATE EXTENSION IF NOT EXISTS vector;

-- User roles enum
CREATE TYPE user_role AS ENUM ('admin', 'caregiver', 'doctor', 'researcher');

-- Memory types enum
CREATE TYPE memory_type AS ENUM ('person', 'place', 'event', 'skill', 'routine', 'object');

-- Connection types enum
CREATE TYPE connection_type AS ENUM ('family', 'friend', 'associated_with', 'located_at', 'temporal', 'emotional');

-- Intervention types enum
CREATE TYPE intervention_type AS ENUM (
    'spaced_repetition',
    'contextual_anchoring',
    'multimedia_reinforcement',
    'emotional_preservation',
    'routine_reminder',
    'navigation_assist'
);

-- Intervention status enum
CREATE TYPE intervention_status AS ENUM ('scheduled', 'delivered', 'completed', 'skipped', 'failed');

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role user_role DEFAULT 'caregiver' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    caregiver_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    diagnosis_date DATE,
    current_stage INTEGER CHECK (current_stage >= 0 AND current_stage <= 7),
    medical_history JSONB,
    medications JSONB,
    mmse_score INTEGER CHECK (mmse_score >= 0 AND mmse_score <= 30),
    moca_score INTEGER CHECK (moca_score >= 0 AND moca_score <= 30),
    cdr_score NUMERIC(3,1) CHECK (cdr_score >= 0 AND cdr_score <= 3),
    notes TEXT,
    emergency_contact JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_patients_caregiver ON patients(caregiver_id);

-- Memories table
CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE NOT NULL,
    type memory_type NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    metadata JSONB,
    recall_strength NUMERIC(5,2) DEFAULT 100.0 NOT NULL CHECK (recall_strength >= 0 AND recall_strength <= 100),
    emotional_weight NUMERIC(3,2) DEFAULT 0.5 NOT NULL CHECK (emotional_weight >= 0 AND emotional_weight <= 1),
    importance INTEGER DEFAULT 5 NOT NULL CHECK (importance >= 1 AND importance <= 10),
    memory_date TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    access_count INTEGER DEFAULT 0 NOT NULL,
    predicted_decay_rate NUMERIC(5,2),
    high_risk BOOLEAN DEFAULT FALSE NOT NULL,
    image_url VARCHAR(500),
    audio_url VARCHAR(500),
    video_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_memories_patient ON memories(patient_id);
CREATE INDEX idx_memories_high_risk ON memories(high_risk) WHERE high_risk = TRUE;

-- Memory connections table
CREATE TABLE IF NOT EXISTS memory_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES memories(id) ON DELETE CASCADE NOT NULL,
    target_id UUID REFERENCES memories(id) ON DELETE CASCADE NOT NULL,
    connection_type connection_type NOT NULL,
    strength NUMERIC(3,2) DEFAULT 1.0 NOT NULL CHECK (strength >= 0 AND strength <= 1),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT no_self_connection CHECK (source_id != target_id)
);

CREATE INDEX idx_connections_source ON memory_connections(source_id);
CREATE INDEX idx_connections_target ON memory_connections(target_id);

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE NOT NULL,
    predicted_stage INTEGER NOT NULL CHECK (predicted_stage >= 0 AND predicted_stage <= 7),
    confidence NUMERIC(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    stage_probabilities JSONB,
    progression_risk VARCHAR(20),
    estimated_progression_months INTEGER,
    mri_scan_id VARCHAR(255),
    cognitive_scores JSONB,
    speech_analysis_id VARCHAR(255),
    behavioral_data JSONB,
    explanation JSONB,
    top_contributing_factors JSONB,
    model_version VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    notes TEXT
);

CREATE INDEX idx_predictions_patient ON predictions(patient_id);
CREATE INDEX idx_predictions_created ON predictions(created_at DESC);

-- Memory decay predictions table
CREATE TABLE IF NOT EXISTS memory_decay_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memory_id UUID REFERENCES memories(id) ON DELETE CASCADE NOT NULL,
    prediction_id UUID REFERENCES predictions(id) ON DELETE SET NULL,
    decay_30_days NUMERIC(5,2) NOT NULL,
    decay_90_days NUMERIC(5,2) NOT NULL,
    decay_180_days NUMERIC(5,2) NOT NULL,
    risk_score NUMERIC(3,2) NOT NULL CHECK (risk_score >= 0 AND risk_score <= 1),
    risk_level VARCHAR(20) NOT NULL,
    days_until_critical INTEGER,
    intervention_recommended BOOLEAN DEFAULT FALSE NOT NULL,
    recommended_intervention_type VARCHAR(50),
    model_version VARCHAR(50) NOT NULL,
    explanation JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_decay_memory ON memory_decay_predictions(memory_id);
CREATE INDEX idx_decay_risk ON memory_decay_predictions(risk_level);

-- Interventions table
CREATE TABLE IF NOT EXISTS interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE NOT NULL,
    memory_id UUID REFERENCES memories(id) ON DELETE SET NULL,
    type intervention_type NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content JSONB,
    scheduled_for TIMESTAMP NOT NULL,
    delivered_at TIMESTAMP,
    completed_at TIMESTAMP,
    status intervention_status DEFAULT 'scheduled' NOT NULL,
    success BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_interventions_patient ON interventions(patient_id);
CREATE INDEX idx_interventions_scheduled ON interventions(scheduled_for);
CREATE INDEX idx_interventions_status ON interventions(status);

-- Intervention results table
CREATE TABLE IF NOT EXISTS intervention_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    intervention_id UUID REFERENCES interventions(id) ON DELETE CASCADE NOT NULL,
    recall_before NUMERIC(5,2),
    recall_after NUMERIC(5,2),
    improvement NUMERIC(5,2),
    time_spent_seconds INTEGER,
    attempts INTEGER DEFAULT 1 NOT NULL,
    hints_used INTEGER DEFAULT 0 NOT NULL,
    patient_feedback TEXT,
    caregiver_notes TEXT,
    emotional_response VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_results_intervention ON intervention_results(intervention_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memories_updated_at BEFORE UPDATE ON memories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_connections_updated_at BEFORE UPDATE ON memory_connections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_interventions_updated_at BEFORE UPDATE ON interventions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
