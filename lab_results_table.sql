-- Lab Results Table for Supabase
-- Stores individual lab test results with mapping to Armgasys variable names

CREATE TABLE lab_results (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Original extracted data
    original_test_name TEXT NOT NULL,
    original_value TEXT NOT NULL,
    unit TEXT,
    reference_range TEXT,
    
    -- Mapped to Armgasys variables
    armgasys_variable_name TEXT,
    armgasys_value TEXT,
    
    -- Metadata
    date_collected TIMESTAMPTZ,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Indexes for performance
    CONSTRAINT unique_client_test_date UNIQUE (client_id, armgasys_variable_name, date_collected)
);

-- Indexes for better query performance
CREATE INDEX idx_lab_results_client_id ON lab_results(client_id);
CREATE INDEX idx_lab_results_armgasys_variable ON lab_results(armgasys_variable_name);
CREATE INDEX idx_lab_results_date_collected ON lab_results(date_collected);

-- Enable Row Level Security (RLS)
ALTER TABLE lab_results ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only access lab results for their organization's clients
-- (This will need to be adjusted based on your auth system)
CREATE POLICY "Users can view lab results" ON lab_results
    FOR SELECT USING (true);  -- Adjust based on your auth requirements

CREATE POLICY "Users can insert lab results" ON lab_results
    FOR INSERT WITH CHECK (true);  -- Adjust based on your auth requirements 