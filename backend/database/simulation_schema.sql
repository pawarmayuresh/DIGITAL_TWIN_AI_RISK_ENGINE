CREATE TABLE IF NOT EXISTS simulations (
  id SERIAL PRIMARY KEY,
  scenario TEXT,
  parameters JSONB,
  started_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  finished_at TIMESTAMP WITH TIME ZONE
);
