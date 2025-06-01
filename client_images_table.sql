-- Client Images Table for Roadmap Visual Content
-- This table stores references to uploaded images for each client

CREATE TABLE IF NOT EXISTS client_images (
    id SERIAL PRIMARY KEY,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    image_type VARCHAR(50) NOT NULL CHECK (image_type IN ('cognitive_test', 'chart', 'screenshot', 'report', 'other')),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    title VARCHAR(255),
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    uploaded_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_client_images_client_id ON client_images(client_id);
CREATE INDEX IF NOT EXISTS idx_client_images_type ON client_images(image_type);
CREATE INDEX IF NOT EXISTS idx_client_images_active ON client_images(is_active);

-- Add RLS (Row Level Security) if needed
-- ALTER TABLE client_images ENABLE ROW LEVEL SECURITY;

-- Comments for documentation
COMMENT ON TABLE client_images IS 'Stores uploaded images and visual content for client roadmaps';
COMMENT ON COLUMN client_images.image_type IS 'Type of image: cognitive_test, chart, screenshot, report, other';
COMMENT ON COLUMN client_images.filename IS 'Unique filename used for storage (UUID-based)';
COMMENT ON COLUMN client_images.original_filename IS 'Original filename as uploaded by user';
COMMENT ON COLUMN client_images.display_order IS 'Order for displaying images in roadmaps (0 = first)'; 