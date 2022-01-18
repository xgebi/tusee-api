-- Your SQL goes here
CREATE TYPE tusee_settings_type AS ENUM ('Boolean', 'Text', 'TextLong');
CREATE TABLE IF NOT EXISTS tusee_settings (
    settings_name			VARCHAR(80) PRIMARY KEY,
	display_name			VARCHAR(100) NOT NULL,
	settings_value_type		tusee_settings_type NOT NULL,
	settings_value			VARCHAR(200) NOT NULL
);

COMMENT ON COLUMN tusee_settings.settings_name IS 'Name of the setting in alphanumeric and underscores';
COMMENT ON COLUMN tusee_settings.display_name IS 'Human readable name of setting';
COMMENT ON COLUMN tusee_settings.settings_value_type IS 'Indicator for how front-end should render setting';
COMMENT ON COLUMN tusee_settings.settings_value IS 'Actual value of the settings';