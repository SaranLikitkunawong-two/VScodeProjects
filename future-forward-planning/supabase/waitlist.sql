-- Run this in the Supabase SQL Editor to create the waitlist table.
-- This is the table the marketing site signup form inserts into.

CREATE TABLE waitlist (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name text NOT NULL,
  email      text NOT NULL,
  phone      text,
  role       text NOT NULL CHECK (role IN ('participant','family','support_coordinator','provider','other')),
  created_at timestamptz DEFAULT now()
);

CREATE INDEX waitlist_email_idx ON waitlist (email);

ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

-- Anonymous (anon key) users can INSERT only — no SELECT/UPDATE/DELETE for anon.
-- You read leads via the Supabase dashboard (authenticated as the project owner).
CREATE POLICY "anon_insert" ON waitlist
  FOR INSERT TO anon
  WITH CHECK (true);
