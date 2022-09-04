ALTER TABLE tusee_events ADD COLUMN description text;
ALTER TABLE tusee_events RENAME COLUMN name TO event_name;