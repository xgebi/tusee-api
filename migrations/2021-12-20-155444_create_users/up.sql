-- Your SQL goes here
CREATE TABLE IF NOT EXISTS tusee_users (
    uuid character varying(200) NOT NULL PRIMARY KEY,
	display_name text NOT NULL ,
	password character varying(500) NOT NULL,
	email character varying(350) UNIQUE NOT NULL ,
	token character varying(350) NOT NULL DEFAULT '',
	expiry_date double precision NOT NULL DEFAULT 0,
	first_login boolean NOT NULL DEFAULT TRUE
)