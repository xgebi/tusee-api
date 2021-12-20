-- Your SQL goes here
CREATE TABLE IF NOT EXISTS tusee_users (
    uuid character varying(200) NOT NULL PRIMARY KEY,
	display_name text,
	password character varying(500) NOT NULL,
	email character varying(350) UNIQUE,
	token character varying(350),
	expiry_date double precision
)