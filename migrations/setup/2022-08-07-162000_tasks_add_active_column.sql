ALTER TABLE tusee_tasks ADD COLUMN active BOOLEAN DEFAULT TRUE;
UPDATE tusee_tasks SET active = TRUE;