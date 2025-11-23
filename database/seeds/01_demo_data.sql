-- Demo Data for NeuroSmriti
-- This creates a complete demo patient with memory graph for testing

-- Note: Run this AFTER running schema.sql

-- Insert demo caregiver user
-- Password: demo123 (bcrypt hash)
INSERT INTO users (id, email, hashed_password, full_name, role, is_active, is_verified)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'demo@neurosmriti.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TdstqKP1C',
    'Dr. Sarah Johnson',
    'caregiver',
    true,
    true
) ON CONFLICT (email) DO NOTHING;

-- Insert demo patient
INSERT INTO patients (
    id,
    caregiver_id,
    full_name,
    date_of_birth,
    gender,
    diagnosis_date,
    current_stage,
    mmse_score,
    moca_score,
    cdr_score,
    notes
)
VALUES (
    '660e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440000',
    'Helen Martinez',
    '1955-03-15',
    'Female',
    '2023-06-15',
    2,
    24,
    22,
    0.5,
    'MCI Stage 2. Patient is independent but showing memory decline. Lives with spouse Mary.'
) ON CONFLICT DO NOTHING;

-- Insert memories for demo patient
-- High-strength memories (family, close relationships)
INSERT INTO memories (id, patient_id, type, name, description, recall_strength, emotional_weight, importance, high_risk)
VALUES
    ('770e8400-e29b-41d4-a716-446655440010', '660e8400-e29b-41d4-a716-446655440001', 'person', 'Mary (Wife)', 'Married for 45 years, lives together', 98.5, 0.99, 10, false),
    ('770e8400-e29b-41d4-a716-446655440011', '660e8400-e29b-41d4-a716-446655440001', 'person', 'Alex (Grandson)', 'Plays baseball, visits on weekends', 72.3, 0.85, 9, true),
    ('770e8400-e29b-41d4-a716-446655440012', '660e8400-e29b-41d4-a716-446655440001', 'person', 'Jennifer (Daughter)', 'Calls every Tuesday evening', 85.7, 0.92, 10, false),
    ('770e8400-e29b-41d4-a716-446655440013', '660e8400-e29b-41d4-a716-446655440001', 'place', 'Home Address', '123 Maple Street, Springfield', 91.2, 0.88, 10, false),
    ('770e8400-e29b-41d4-a716-446655440014', '660e8400-e29b-41d4-a716-446655440001', 'place', 'Grocery Store', 'Corner market, goes every Saturday', 68.4, 0.45, 6, true),
    ('770e8400-e29b-41d4-a716-446655440015', '660e8400-e29b-41d4-a716-446655440001', 'event', 'Wedding Anniversary', 'June 12th every year', 79.1, 0.94, 9, false),
    ('770e8400-e29b-41d4-a716-446655440016', '660e8400-e29b-41d4-a716-446655440001', 'event', 'Alex Birthday', 'Grandson birthday - March 3rd', 65.8, 0.87, 8, true),
    ('770e8400-e29b-41d4-a716-446655440017', '660e8400-e29b-41d4-a716-446655440001', 'routine', 'Morning Coffee', 'Coffee with Mary every morning at 7am', 88.9, 0.76, 7, false),
    ('770e8400-e29b-41d4-a716-446655440018', '660e8400-e29b-41d4-a716-446655440001', 'routine', 'Medication Schedule', 'Blood pressure pill at 8am', 71.2, 0.58, 10, true),
    ('770e8400-e29b-41d4-a716-446655440019', '660e8400-e29b-41d4-a716-446655440001', 'skill', 'Playing Piano', 'Used to play every evening', 54.3, 0.82, 6, true)
ON CONFLICT DO NOTHING;

-- Insert memory connections (relationships between memories)
INSERT INTO memory_connections (source_id, target_id, connection_type, strength, description)
VALUES
    -- Family relationships
    ('770e8400-e29b-41d4-a716-446655440010', '770e8400-e29b-41d4-a716-446655440012', 'family', 0.95, 'Mary is Jennifer''s mother'),
    ('770e8400-e29b-41d4-a716-446655440012', '770e8400-e29b-41d4-a716-446655440011', 'family', 0.98, 'Jennifer is Alex''s mother'),
    ('770e8400-e29b-41d4-a716-446655440010', '770e8400-e29b-41d4-a716-446655440011', 'family', 0.90, 'Mary is Alex''s grandmother'),

    -- Location associations
    ('770e8400-e29b-41d4-a716-446655440010', '770e8400-e29b-41d4-a716-446655440013', 'located_at', 0.99, 'Mary lives at home'),
    ('770e8400-e29b-41d4-a716-446655440017', '770e8400-e29b-41d4-a716-446655440013', 'located_at', 0.95, 'Morning coffee at home'),

    -- Temporal connections
    ('770e8400-e29b-41d4-a716-446655440015', '770e8400-e29b-41d4-a716-446655440010', 'temporal', 0.96, 'Anniversary with Mary'),
    ('770e8400-e29b-41d4-a716-446655440016', '770e8400-e29b-41d4-a716-446655440011', 'temporal', 0.92, 'Alex''s birthday'),

    -- Routine associations
    ('770e8400-e29b-41d4-a716-446655440017', '770e8400-e29b-41d4-a716-446655440010', 'associated_with', 0.88, 'Coffee with Mary'),
    ('770e8400-e29b-41d4-a716-446655440014', '770e8400-e29b-41d4-a716-446655440010', 'associated_with', 0.75, 'Shops with Mary')
ON CONFLICT DO NOTHING;

-- Insert sample prediction
INSERT INTO predictions (
    id,
    patient_id,
    predicted_stage,
    confidence,
    stage_probabilities,
    progression_risk,
    estimated_progression_months,
    cognitive_scores,
    top_contributing_factors,
    model_version,
    model_type,
    notes
)
VALUES (
    '880e8400-e29b-41d4-a716-446655440020',
    '660e8400-e29b-41d4-a716-446655440001',
    2,
    0.87,
    '{"0": 0.02, "1": 0.05, "2": 0.87, "3": 0.04, "4": 0.01, "5": 0.01, "6": 0.00, "7": 0.00}'::jsonb,
    'medium',
    18,
    '{"mmse": 24, "moca": 22, "cdr": 0.5}'::jsonb,
    '["Word-finding difficulty increased 40% in past 3 months", "GPS confusion at familiar intersection twice this week", "Sleep REM decreased 25%"]'::jsonb,
    'v1.0.0',
    'multimodal_transformer',
    'Based on cognitive scores, speech analysis, and behavioral patterns'
) ON CONFLICT DO NOTHING;

-- Insert memory decay predictions for high-risk memories
INSERT INTO memory_decay_predictions (
    memory_id,
    prediction_id,
    decay_30_days,
    decay_90_days,
    decay_180_days,
    risk_score,
    risk_level,
    days_until_critical,
    intervention_recommended,
    recommended_intervention_type,
    model_version
)
VALUES
    ('770e8400-e29b-41d4-a716-446655440011', '880e8400-e29b-41d4-a716-446655440020', 68.2, 61.5, 52.3, 0.92, 'high', 12, true, 'spaced_repetition', 'v1.0.0'),
    ('770e8400-e29b-41d4-a716-446655440016', '880e8400-e29b-41d4-a716-446655440020', 61.4, 54.8, 45.2, 0.87, 'high', 18, true, 'contextual_anchoring', 'v1.0.0'),
    ('770e8400-e29b-41d4-a716-446655440018', '880e8400-e29b-41d4-a716-446655440020', 66.8, 59.2, 48.7, 0.89, 'high', 15, true, 'routine_reminder', 'v1.0.0'),
    ('770e8400-e29b-41d4-a716-446655440014', '880e8400-e29b-41d4-a716-446655440020', 63.5, 57.1, 47.9, 0.81, 'medium', 22, true, 'navigation_assist', 'v1.0.0'),
    ('770e8400-e29b-41d4-a716-446655440019', '880e8400-e29b-41d4-a716-446655440020', 49.7, 42.3, 31.8, 0.95, 'critical', 8, true, 'multimedia_reinforcement', 'v1.0.0')
ON CONFLICT DO NOTHING;

-- Insert sample interventions
INSERT INTO interventions (
    patient_id,
    memory_id,
    type,
    title,
    description,
    content,
    scheduled_for,
    status
)
VALUES
    (
        '660e8400-e29b-41d4-a716-446655440001',
        '770e8400-e29b-41d4-a716-446655440011',
        'spaced_repetition',
        'Remember Alex''s Baseball',
        'Help strengthen memory of grandson''s weekly baseball games',
        '{"photos": ["alex_baseball.jpg"], "questions": ["What sport does Alex play?", "When are Alex''s games?"]}'::jsonb,
        NOW() + INTERVAL '2 hours',
        'scheduled'
    ),
    (
        '660e8400-e29b-41d4-a716-446655440001',
        '770e8400-e29b-41d4-a716-446655440018',
        'routine_reminder',
        'Morning Medication Reminder',
        'Daily reminder for blood pressure medication',
        '{"time": "08:00", "medication": "Lisinopril 10mg", "with_food": true}'::jsonb,
        NOW() + INTERVAL '18 hours',
        'scheduled'
    )
ON CONFLICT DO NOTHING;

-- Success message
SELECT 'Demo data inserted successfully! You can now log in with:' AS message
UNION ALL
SELECT 'Email: demo@neurosmriti.com' AS message
UNION ALL
SELECT 'Password: demo123' AS message;
