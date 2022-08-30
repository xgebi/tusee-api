CREATE TABLE IF NOT EXISTS tusee_notes (
    note_uuid character varying(200) NOT NULL PRIMARY KEY,
	user_uuid character varying(200) NOT NULL,
	title text,
	note text
);