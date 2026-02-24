CREATE TABLE IF NOT EXISTS disasters (
  id SERIAL PRIMARY KEY,
  type TEXT NOT NULL,
  intensity TEXT,
  payload JSONB,
  generated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
